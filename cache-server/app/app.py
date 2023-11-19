import os
from datetime import datetime, date
from json import JSONEncoder
from typing import Optional, Union, Any
from urllib.parse import quote_plus
from bson import ObjectId
from flask import Flask, current_app, request, jsonify
from pymongo import MongoClient, ASCENDING
from pymongo.cursor import Cursor


DATETIME_FORMATS = [
    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M:%S",
]
DATE_FORMAT = "%Y-%m-%d"


class MongoDBEnhancedEncoder(JSONEncoder):
    """
    This is an enhancement over a Flask's JSONEncoder but with
    adding the encoding of an ObjectId to string, and custom
    encodings for the date and datetime types.
    """

    def default(self, o: Any) -> Any:
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime):
            return o.strftime(DATETIME_FORMATS[0])
        elif isinstance(o, date):
            return o.strftime(DATE_FORMAT)
        return super().default(o)


def sort_and_page(cursor: Cursor, sort: Optional[Union[dict, list]], skip: Optional[int], limit: Optional[int]):
    """
    Returns a modified cursor with a specific sorting, offset and limit.
    :param cursor: The cursor.
    :param sort: The sort.
    :param skip: The skip.
    :param limit: The limit.
    :return: The new cursor.
    """

    if sort:
        cursor = cursor.sort(sort)
    if skip is not None and skip > 0:
        cursor = cursor.skip(skip)
    if limit is not None and limit > 0:
        cursor = cursor.limit(limit)
    return cursor


class CacheApp(Flask):
    """
    The cache app we use.
    """

    json_encoder: type = MongoDBEnhancedEncoder

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mongo_client = self._make_client()
        self._db = self._mongo_client[os.environ["DB_NAME"]]
        self._use_transactions = os.getenv('MONGODB_TRANSACTIONS') == 'yes'
        try:
            self._page_size = int(os.environ['PAGE_SIZE'])
            if self._page_size < 1:
                self._page_size = 10
        except:
            self._page_size = 10

    def _make_client(self):
        """
        Builds a MongoDB client for this server, based on given
        environment variables.
        """

        server_url = os.getenv("MONGODB_URL")
        if not server_url:
            server_url = "mongodb://%s:%s@%s:%s" % (
                quote_plus(os.environ["MONGODB_USER"]),
                quote_plus(os.environ["MONGODB_PASSWORD"]),
                os.getenv("MONGODB_HOST", "localhost"),
                os.getenv("MONGODB_PORT", "27017")
            )
        return MongoClient(server_url)

    @property
    def mongo_client(self):
        return self._mongo_client

    @property
    def database(self):
        return self._db

    @property
    def tokens_metadata(self):
        return self._db["tokens_metadata"]

    def sort_and_page(self, cursor: Cursor, sort: Optional[Union[dict, list]], skip: Optional[int]):
        """
        Applies sorting/paging based on the current limit.
        :param cursor: The cursor
        :param sort: The sort criteria.
        :param skip: The skip.
        :return:
        """

        return sort_and_page(cursor, sort, skip, self._page_size)

    def get_skip(self):
        """
        Gets the skip value to use.
        :return: The skip value to use.
        """

        try:
            page = int(request.args.get("page"))
            if page < 0:
                page = 0
        except:
            page = 0
        return page * self._page_size

    def mongo_session(self, f):
        """
        A decorator that opens a mongodb transactional session
        if the server works with transactions.
        :param f: The function to wrap.
        """

        def wrapped(*args, **kwargs):
            if self._use_transactions:
                with self._mongo_client.start_session() as session:
                    # Review: Perhaps should I care about read and
                    # write concerns? Not sure.
                    with session.start_transaction():
                        result = f(*args, session_kwargs={"session": session}, **kwargs)
                        session.commit_transaction()
                        return result
            else:
                return f(*args, session_data={}, **kwargs)

        return wrapped


app = CacheApp("cache-server")
current_app: CacheApp


@app.route("/brands", methods=["GET"])
@app.mongo_session
def get_brands(session_kwargs):
    text = request.args.get("text")
    criteria = {"$text": {"search": text}} if text else {}
    brands = current_app.sort_and_page(
        current_app.tokens_metadata.find(criteria, **session_kwargs),
        sort=[("metadata.name", ASCENDING)], skip=current_app.get_skip()
    )
    return jsonify({"brands": brands})
