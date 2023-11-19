import functools
import os
from datetime import datetime, date
from typing import Optional, Union, Any
from urllib.parse import quote_plus
from bson import ObjectId
from flask import Flask, current_app, request, jsonify
from flask.json.provider import DefaultJSONProvider
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.cursor import Cursor


DATETIME_FORMATS = [
    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M:%S",
]
DATE_FORMAT = "%Y-%m-%d"


class MongoDBEnhancedProvider(DefaultJSONProvider):
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

    json_provider_class: type = MongoDBEnhancedProvider

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
    def page_size(self):
        return self._page_size

    @property
    def tokens_metadata(self):
        return self._db["tokens_metadata"]

    @property
    def balances(self):
        return self._db["balances"]

    @property
    def deals(self):
        return self._db["deals"]

    @property
    def metaverse_parameters(self):
        return self._db["metaverse_parameters"]

    @property
    def metaverse_permissions(self):
        return self._db["metaverse_permissions"]

    @property
    def brand_permissions(self):
        return self._db["brand_permissions"]

    @property
    def sponsors(self):
        return self._db["sponsors"]

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

        @functools.wraps(f)
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
                return f(*args, session_kwargs={}, **kwargs)

        return wrapped


app = CacheApp("cache-server")
current_app: CacheApp


@app.route("/brands", methods=["GET"])
@app.mongo_session
def get_brands(session_kwargs: dict):
    text = request.args.get("text")
    criteria = {"token_group": "nft", "metadata.properties.type": "brand"}
    if text:
        criteria |= {"$text": {"search": text}}
    brands = current_app.sort_and_page(
        current_app.tokens_metadata.find(criteria, **session_kwargs),
        sort=[("metadata.name", ASCENDING)], skip=current_app.get_skip()
    )
    return jsonify({"brands": list(brands)})


@app.route("/brands/<string:brand>/tokens", methods=["GET"])
@app.mongo_session
def get_brand_tokens(brand: str, session_kwargs: dict):
    text = request.args.get("text")
    criteria = {"token_group": "ft", "brand": brand}
    if text:
        criteria |= {"$text": {"search": text}}
    tokens = current_app.sort_and_page(
        current_app.tokens_metadata.find(criteria, **session_kwargs),
        sort=[("metadata.name", ASCENDING)], skip=current_app.get_skip()
    )
    return jsonify({"tokens": list(tokens)})


@app.route("/balances/<string:owner>", methods=["GET"])
@app.mongo_session
def get_balances(owner: str, session_kwargs: dict):
    criteria = {"owner": owner}
    tokens = request.args.get("tokens", "")
    if tokens:
        tokens = tokens.split(",")[:current_app.page_size]
        criteria |= {"token": {"$in": tokens}}
    balances = current_app.sort_and_page(
        current_app.balances.find(criteria, **session_kwargs),
        sort=[("token", ASCENDING)], skip=current_app.get_skip()
    )
    return jsonify({"balances": list(balances)})


@app.route("/deals/<string:dealer>", methods=["GET"])
@app.mongo_session
def get_deals(dealer: str, session_kwargs: dict):
    criteria = {"$or": [{"receiver": dealer}, {"emitter": dealer}]}
    deals = current_app.sort_and_page(
        current_app.deals.find(criteria, **session_kwargs),
        sort=[("index", DESCENDING)], skip=current_app.get_skip()
    )
    return jsonify({"deals": list(deals)})


@app.route("/permissions/<string:user>", methods=["GET"])
@app.mongo_session
def get_permissions(user: str, session_kwargs: dict):
    criteria = {"user": user, "value": True}
    permissions = current_app.sort_and_page(
        # Don't worry: It WILL be sorted on front-end.
        current_app.metaverse_permissions.find(criteria, **session_kwargs),
        sort=[], skip=current_app.get_skip()
    )
    return jsonify({"permissions": list(permissions)})


@app.route("/brands/<string:brand>/permissions/<string:user>", methods=["GET"])
@app.mongo_session
def get_brand_permissions(brand: str, user: str, session_kwargs: dict):
    criteria = {"user": user, "value": True, "brand": brand}
    permissions = current_app.sort_and_page(
        # Don't worry: It WILL be sorted on front-end.
        current_app.brand_permissions.find(criteria, **session_kwargs),
        sort=[], skip=current_app.get_skip()
    )
    return jsonify({"permissions": list(permissions)})


@app.route("/brands/<string:brand>/sponsors", methods=["GET"])
@app.mongo_session
def get_brand_sponsors(brand: str, session_kwargs: dict):
    criteria = {"brand": brand, "sponsored": True}
    sponsors = current_app.sort_and_page(
        current_app.sponsors.find(criteria, **session_kwargs),
        sort=[], skip=current_app.get_skip()
    )
    return jsonify({"sponsors": list(sponsors)})


@app.route("/parameters", methods=["GET"])
@app.mongo_session
def get_parameters(session_kwargs: dict):
    parameters = current_app.sort_and_page(
        current_app.metaverse_parameters.find({}, **session_kwargs),
        sort=[], skip=current_app.get_skip()
    )
    return jsonify({"parameters": list(parameters)})


@app.route("/sponsors/<string:sponsor>", methods=["GET"])
@app.mongo_session
def get_sponsors(sponsor: str, session_kwargs: dict):
    criteria = {"sponsor": sponsor, "sponsored": True}
    sponsors = current_app.sort_and_page(
        current_app.sponsors.find(criteria, **session_kwargs),
        sort=[], skip=current_app.get_skip()
    )
    return jsonify({"sponsors": list(sponsors)})
