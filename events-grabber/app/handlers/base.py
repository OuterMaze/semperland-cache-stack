import json
import logging
from typing import Union
from pymongo import MongoClient
from web3.contract import Contract
from web3.datastructures import AttributeDict
from urllib.request import urlopen


LOGGER = logging.getLogger("grabber")
LOGGER.setLevel(logging.INFO)


class EventList:
    """
    An event list, hierarchically sorted.
    """

    def __init__(self):
        self._events = {}

    def add_event(self, event: dict, handler: "ContractEventHandler"):
        """
        Adds an event to the structure
        :param event: The event to add.
        :param handler: The handler to add.
        """

        block_number = int(event["blockNumber"])
        transaction_index = int(event["transactionIndex"])
        log_index = int(event["logIndex"])

        self._events.setdefault(block_number, {}).setdefault(transaction_index, {})[log_index] = (
            event, handler
        )

    def sorted_events(self):
        """
        Iterates over the events.
        :return: An iterator over the events.
        """

        for block_number in sorted(self._events.keys()):
            block_number_events = self._events[block_number]
            for transaction_number in sorted(block_number_events.keys()):
                transaction_number_events = block_number_events[transaction_number]
                for log_number in sorted(transaction_number_events.keys()):
                    yield transaction_number_events[log_number]


class ContractEventHandler:
    """
    A contract handler is used to collect and process the events of
    a specified contract. For example, a handler may focus on the
    TransferSingle/Batch of an ERC-1155 while other handlers might
    focus on the approval-related events in that contract.
    """

    def __init__(self, contract: Contract):
        self._contract = contract
        self._name = "<unnamed>"

    @property
    def name(self):
        return self._name

    def get_event_names(self):
        raise NotImplementedError

    @property
    def contract(self):
        return self._contract

    @property
    def web3(self):
        return self._contract.w3

    def _is_zero(self, value: Union[str, int]):
        """
        Tests whether a value is a numeric 0 or 0.0, or perhaps
        a string representation of a 0 numeric value in any base.
        :param value: The value to test.
        :return: Whether it is zero or not.
        """

        if value == 0:
            return True

        for b in range(2, 37):
            try:
                if int(value, b) == 0:
                    return True
                else:
                    break
            except:
                pass

        return False

    def _get_arg(self, args: AttributeDict, key: str):
        """
        Gets an argument from the args, by trying both `{key}` and `_{key}`
        as the key to test.
        :param args: The args to get an argument from.
        :param key: The key to retrieve.
        :return:
        """

        if key in args:
            return args[key]
        else:
            return args.get("_" + key)

    def _prune_event(self, event):
        """
        Keeps only some relevant fields of an event.
        :param event: The event to prune.
        :return: The pruned event.
        """

        return {**{
            k: v for k, v in event.items() if k in {"blockNumber", "transactionIndex", "logIndex",
                                                    "args", "event"}
        }}

    def collect_events(self, start_block: int, end_block: int, events: EventList):
        """
        Collects all the relevant events for this handler.
        """

        for event_name in self.get_event_names():
            LOGGER.info(f"Processing records for event: {self.name}:{event_name} in range: {start_block}:{end_block}")
            event_filter = getattr(self._contract.events, event_name).create_filter(
                fromBlock=start_block, toBlock=end_block
            )
            for event in event_filter.get_all_entries():
                events.add_event(self._prune_event(event), self)

    def process_event(self, event: dict):
        """
        Processes an event accordingly.
        :param event: The event to process.
        """

        raise NotImplementedError


class MongoDBContractEventHandler(ContractEventHandler):
    """
    This contract handler has access to MongoDB features.
    """

    def __init__(self, contract: Contract, client: MongoClient, db_name: str, session_kwargs: dict):
        super().__init__(contract)
        self._client = client
        self._session_kwargs = session_kwargs
        self._db_name = db_name
        self._db = client[db_name]

    @property
    def client(self):
        """
        The MongoDB client.
        """

        return self._client

    @property
    def db(self):
        """
        The MongoDB database.
        """

        return self._db

    @property
    def db_name(self):
        """
        The database name.
        """

        return self._db_name

    @property
    def client_session_kwargs(self):
        """
        The current session (with an open transaction), optionally.
        """

        return self._session_kwargs


"""
This class has the following requirements in whatever is used as the underlying
database:

1. "tokens_metadata" collection must be indexed:
   - uniquely by `token_id`.
   - non-uniquely br `brand_id` (ordering does not matter).
   - non-uniquely by `token_type` (ordering does not matter).
"""


class MetaverseRelatedContractEventHandler(MongoDBContractEventHandler):
    """
    This subclass allows a contract handler to invoke the Metaverse's
    `tokenURI` method and retrieve its JSON content. If there's an
    error trying to retrieve the JSON content, then an incomplete
    metadata will be returned instead. Also, allows interacting with
    the metaverse's parameters.
    """

    TOKENS_METADATA = "tokens_metadata"
    METAVERSE_PARAMETERS = "metaverse_parameters"

    def __init__(self, contract: Contract, metaverse_contract: Contract,
                 client: MongoClient, db_name: str, session_kwargs: dict):
        super().__init__(contract, client, db_name, session_kwargs)
        self._metaverse_contract = metaverse_contract
        self._metaverse_parameters = self.db[self.METAVERSE_PARAMETERS]
        self._tokens_metadata = self.db[self.TOKENS_METADATA]

    def _get_json(self, url: str) -> dict:
        """
        Gets the associated JSON content from a URL.
        :param url: The URL to retrieve.
        :return: The JSON contents.
        """

        try:
            with urlopen(url) as response:
                if response.headers["Content-Type"] is None:
                    raise Exception("Invalid content type")
                return json.loads(response.read())
        except:
            return {"name": "INVALID", "description": "INVALID", "image": "about:blank", "properties": {}}

    def _get_metadata(self, token_id: int):
        """
        Gets the associated JSON content from a token id.
        :param token_id: The token id to retrieve the  metadata from.
        :return: The JSON contents.
        """

        url = self._metaverse_contract.functions.tokenURI(token_id).call()
        if url == "":
            return {"name": "UNKNOWN", "description": "UNKNOWN", "image": "about:blank", "properties": {}}
        return self._get_json(url)

    def _download_metadata(self, token_id: int):
        """
        Downloads the associated JSON content from a token id. The content
        is downloaded in the metadata table.
        :param token_id: The id of the token whose metadata is being downloaded.
        :param token_type: The token type.
        """

        data = self._get_metadata(token_id)
        data["name"] = (data.get("name") or "").strip()
        data["description"] = (data.get("description") or "").strip()
        data["image"] = (data.get("image") or "").strip()
        document = {
            "token": "0x%064x" % token_id,
            "metadata": data,
            "token_group": "nft"
        }
        token_num = int(token_id)
        if token_num & (1 << 255):
            # FTs are associated to the system or to a brand.
            # So here we extract the brand (where 0x000...000
            # stands for the SYSTEM, actually).
            #
            # Also, the token is marked as FT instead of NFT.
            brand_num = (token_num >> 64) & ((1 << 160) - 1)
            document["brand"] = self.contract.w3.to_checksum_address("0x%040x" % brand_num)
            document["token_group"] = "ft"
        elif data.get("properties", {}).get("type") == "brand":
            # We extract the brand itself.
            document["brand"] = self.contract.w3.to_checksum_address("0x%040x" % token_num)
        self._tokens_metadata.replace_one({
            "token": "0x%064x" % token_id
        }, document, upsert=True, **self.client_session_kwargs)

    def _set_parameter(self, key, value):
        """
        Sets or updates a parameter in the blockchain.
        :param key: The parameter name.
        :param value: The parameter value. Not a specific type.
        """

        self._metaverse_parameters.replace_one({
            "key": key
        }, {
            "key": key, "value": value
        }, upsert=True, **self.client_session_kwargs)


class ContractEventHandlers:
    """
    This class manages a whole set of contract handlers to perform
    a full lifecycle of event extractions.
    """

    def __init__(self, *args):
        """
        Creates the instance with a list of handlers.
        :param args: The handlers, one by one, to specify.
        """

        self._handlers = args

    def process_events(self, start_block: int, end_block: int):
        """
        Processes all the events from a start block number to the
        end block number, both inclusive.
        :param start_block: The start block index.
        :param end_block: The end block index (both inclusive).
        """

        events = EventList()
        for handler in self._handlers:
            LOGGER.info(f"Collecting all the events for handler: {handler.name} in range: {start_block}:{end_block}")
            handler.collect_events(start_block, end_block, events)
        for event, handler in events.sorted_events():
            LOGGER.info(f"Processing event {event['blockNumber']}:{event['transactionIndex']}:{event['logIndex']} "
                        f"with handler: {handler.name}")
            handler.process_event(event)
