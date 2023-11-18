import os
import logging
from urllib.parse import quote_plus
from ilock import ILock
from pymongo import MongoClient
from web3 import Web3, HTTPProvider
from runner import run_all


logging.basicConfig()
LOGGER = logging.getLogger("grabber:main-loop")
LOGGER.setLevel(logging.INFO)


def main(mongodb_server_url: str, db_name: str, gateway_url: str, use_transactions: bool,
         metaverse_contract_address: str):
    """
    The full SemperLand events grabber.
    :param mongodb_server_url: The URL of the MongoDB server.
    :param db_name: The database name
    :param gateway_url: The URL of the EVM Gateway to use.
    :param use_transactions: Whether to use transactions or not.
    :param metaverse_contract_address: The address of the metaverse contract.
    """

    try:
        LOGGER.info("Started")
        with ILock("semperland.cache"):
            LOGGER.info("Creating client")
            client = MongoClient(mongodb_server_url)
            LOGGER.info("Running all the loop")
            run_all(client, db_name, Web3(HTTPProvider(gateway_url)), use_transactions, metaverse_contract_address)
    finally:
        LOGGER.info("Ended")


if __name__ == "__main__":
    server_url = os.getenv("MONGODB_URL")
    if not server_url:
        server_url = "mongodb://%s:%s@%s:%s" % (
            quote_plus(os.environ["MONGODB_USER"]),
            quote_plus(os.environ["MONGODB_PASSWORD"]),
            os.getenv("MONGODB_HOST", "localhost"),
            os.getenv("MONGODB_PORT", "27017")
        )

    main(server_url, os.environ["DB_NAME"], os.environ["GATEWAY_URL"], os.getenv('MONGODB_TRANSACTIONS') == 'yes',
         os.environ["METAVERSE_CONTRACT_ADDRESS"])
