import os
from urllib.parse import quote_plus
from flask import Flask
from pymongo import MongoClient


class CacheApp(Flask):
    """
    The cache app we use.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mongo_client = self._make_client()
        self._db = self._mongo_client[os.environ["DB_NAME"]]
        self._use_transactions = os.getenv('MONGODB_TRANSACTIONS') == 'yes'

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
