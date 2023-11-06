from typing import Union, Dict, Tuple
from pymongo import MongoClient
from pymongo.client_session import ClientSession
from web3.contract import Contract
from web3.datastructures import AttributeDict


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

    def get_events(self):
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

    def collect_events(self, start_block: str, end_block: str, events: EventList):
        """
        Collects all the relevant events for this handler.
        """

        for event_name in self.get_events():
            event_filter = getattr(self._contract.events, event_name).createFilter(
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

    def __init__(self, contract: Contract, client: MongoClient, db_name: str, session: ClientSession):
        super().__init__(contract)
        self._client = client
        self._session = session
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
    def client_session(self):
        """
        The current session (with an open transaction).
        """

        return self._session


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

    def process_events(self, start_block: str, end_block: str):
        """
        Processes all the events from a start block number to the
        end block number, both inclusive.
        :param start_block: The start block index.
        :param end_block: The end block index (both inclusive).
        """

        events = EventList()
        for handler in self._handlers:
            handler.collect_events(start_block, end_block, events)
        for event, handler in events.sorted_events():
            handler.process_event(event)
