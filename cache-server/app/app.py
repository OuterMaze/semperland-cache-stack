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


app = Flask("cache-server")


@app.route("/brands", methods=["GET"])
def get_brands():
    pass
