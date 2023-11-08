import os
from urllib.parse import quote_plus
from ilock import ILock
from pymongo import MongoClient
from web3 import Web3, HTTPProvider
from runner import run_all


def main(mongodb_server_url: str, db_name: str, gateway_url: str, metaverse_contract_address: str):
    """
    The full SemperLand events grabber.
    :param mongodb_server_url: The URL of the MongoDB server.
    :param db_name: The database name
    :param gateway_url: The URL of the EVM Gateway to use.
    :param metaverse_contract_address: The address of the metaverse contract.
    """

    with ILock("semperland.cache"):
        client = MongoClient(mongodb_server_url)
        run_all(client, db_name, Web3(HTTPProvider(gateway_url)), metaverse_contract_address)


if __name__ == "__main__":
    mongodb_server_url = os.getenv("MONGODB_URL")
    if not mongodb_server_url:
        mongodb_server_url = "mongodb://%s:%s@%s:%s" % (
            quote_plus(os.environ["MONGODB_USER"]),
            quote_plus(os.environ["MONGODB_PASSWORD"]),
            os.getenv("MONGODB_HOST", "localhost"),
            os.getenv("MONGODB_PORT", "27017")
        )

    main(mongodb_server_url, os.environ["DB_NAME"], os.environ["GATEWAY_URL"],
         os.environ["METAVERSE_CONTRACT_ADDRESS"])
