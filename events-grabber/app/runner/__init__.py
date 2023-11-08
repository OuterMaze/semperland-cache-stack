from typing import Optional
from web3 import Web3
from pymongo import MongoClient
from pymongo.client_session import ClientSession
from .prepare import make_indices
from ..handlers import make_handlers
from ..contracts import get_contracts


def run_all(client: MongoClient, db_name: str, web3: Web3,
            metaverse_contract_address: str):
    """
    Runs a whole cycle of events retrieval.
    :param client: The client to use.
    :param db_name: The name of the database to use.
    :param web3: The Web3 client to use.
    :param metaverse_contract_address: The address of the metaverse contract.
    """

    make_indices(client, db_name)
    with client.start_session() as session:
        # Review: Perhaps should I care about read and
        # write concerns? Not sure.
        with session.start_transaction():
            # Get the last block and then the start block.
            last_block = _get_last_processed_block_number(client, db_name, session)
            start_block = 0 if last_block is None else last_block + 1
            # Also get the end block.
            end_block = web3.eth.block_number

            # Process the events between start and end block,
            # both limits inclusive.
            contracts = get_contracts(web3, metaverse_contract_address)
            make_handlers(
                client, db_name, session, contracts["metaverse"],
                contracts["brand_registry"], contracts["economy"],
                contracts["sponsor_registry"], contracts["currency_definition_plugin"]
            ).process_events(start_block, end_block)

            # Set the new last block.
            _set_last_processed_block(client, db_name, session, end_block)


def _get_last_processed_block_number(client: MongoClient, db_name: str, session: ClientSession) -> Optional[int]:
    """
    Gets the last processed block, from previous calls.
    :param client: The MongoDB client.
    :param db_name: The database name.
    :param session: The MongoDB session.
    :return: The last processed block number, or None if not present.
    """

    collection = client[db_name]["state"]
    record = collection.find_one(session=session)
    if not record:
        return None
    last_block = record.get("last_block")
    if last_block:
        return int(last_block)
    return None


def _set_last_processed_block(client: MongoClient, db_name: str, session: ClientSession, block_number: int):
    """
    Sets the last processed block, for future calls.
    :param client: The MongoDB client.
    :param db_name: The database name.
    :param session: The MongoDB session.
    :param block_number: The block number.
    """

    collection = client[db_name]["state"]
    collection.replace_one({}, {"last_block": str(block_number)},
                           upsert=True, session=session)
