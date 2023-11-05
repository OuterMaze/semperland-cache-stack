from typing import List
from pymongo import MongoClient
from pymongo.client_session import ClientSession
from pymongo.collection import Collection
from web3 import Web3
from web3.datastructures import AttributeDict
from .abi import ABI
from ..contract_handler import ContractHandler


EVENTS = ["DealStarted", "DealAccepted", "DealConfirmed", "DealBroken",
          "TransferSingle", "TransferBatch"]


class EconomyHandler(ContractHandler):
    """
    The Economy contract stands for two different things to cache:
    - Transfers (single and batch).
    - Deals (start, accept, confirm and break).
    """

    def get_abi(self):
        return ABI

    def get_events(self):
        return EVENTS

    def __call__(self, client: MongoClient, db: str, session: ClientSession, event: AttributeDict, web3: Web3):
        """
        Intended to process logs which come from a TransferSingle(address indexed, address
        indexed, uint256 token, uint256 amount) and TransferBatch(address indexed, address
        indexed, uint256[] tokens, uint256[] amounts). The address 0x0 will not be taken
        into account (in the 1st argument means "mint", and in the second argument means
        "burn"). The result involves (the addresses, the transferred (token, amount) pairs,
        the final balances of each address on each involved token).
        :param client: The MongoDB client to use.
        :param db: The database to use.
        :param session: The current MongoDB session.
        :param event: The event being processed.
        :param web3: The current Web3 client - not used here.
        :return: A response that tells the cache updates and event details.
        """

        event_name = event['event']
        args = event['args']
        from_ = self._get_arg(args, 'from')
        to = self._get_arg(args, 'to')
        tokens_collection = client[db]["tokens"]
        deals_collection = client[db]["deals"]

        if event_name == 'TransferSingle':
            id_ = hex(self._get_arg(args, 'id') or 0)
            value = self._get_arg(args, 'value') or 0
            self._handle_transfer_single(tokens_collection, session, from_, to, id_, value)
        elif event_name == 'TransferBatch':
            ids_ = [hex(k) for k in self._get_arg(args, 'ids') or []]
            values = self._get_arg(args, 'values') or []
            self._handle_transfer_batch(tokens_collection, session, from_, to, ids_, values)
        elif event_name == 'DealStarted':
            self._handle_deal_started(self._get_arg(args, 'dealId'),
                                      self._get_arg(args, 'emitter'),
                                      self._get_arg(args, 'receiver'),
                                      deals_collection)
        elif event_name == 'DealAccepted':
            self._handle_deal_accepted(self._get_arg(args, 'dealId'),
                                       deals_collection)
        elif event_name == 'DealConfirmed':
            self._handle_deal_confirmed(self._get_arg(args, 'dealId'),
                                        deals_collection)
        elif event_name == 'DealBroken':
            self._handle_deal_broken(self._get_arg(args, 'dealId'),
                                     deals_collection)

    def _balance_change(self, from_: str, id_: str, value: int, collection: Collection, session: ClientSession):
        """
        Decrements the balance of a given (owner, token) entry.
        :param from_: The owner.
        :param id_: The token id.
        """

        from_entry = collection.find_one({
            "owner": from_,
            "token": id_
        }, session=session) or {}
        from_balance = int(from_entry.get('amount') or '0')
        from_balance += value
        from_balance_str = str(from_balance)
        collection.replace_one({
            "owner": from_,
            "token": id_
        }, {
            "owner": from_,
            "token": id_,
            "amount": from_balance_str
        }, session=session, upsert=True)

    def _handle_transfer_single(self, collection: Collection, session: ClientSession,
                                from_: str, to: str, id_: str, value: int):
        """
        Processes a TransferSingle event, in a similar way to how ERC-20 processes
        its Transfer event, but also telling the token id.
        :param collection: The involved cache collection.
        :param session: The current MongoDB session.
        :param from_: The token sender. It will be zero on mint.
        :param to: The token receiver. It will be zero on burn.
        :param id_: The token id.
        :param value: The token amount.
        """

        if not self._is_zero(from_):
            self._balance_change(from_, id_, -value, collection, session)
        if not self._is_zero(to):
            self._balance_change(to, id_, value, collection, session)

    def _handle_transfer_batch(self, collection: Collection, session: ClientSession,
                               from_: str, to: str, ids: List[str], values: List[int]):
        """
        Processes a TransferBatch event, which involves per-token updates.
        :param collection: The involved cache collection.
        :param session: The current MongoDB session.
        :param from_: The token sender. It will be zero on mint.
        :param to: The token receiver. It will be zero on burn.
        :param ids: The token ids.
        :param values: The respective token amounts.
        """

        if not self._is_zero(from_):
            for id_, value in zip(ids, values):
                self._balance_change(from_, id_, -value, collection, session)
        if not self._is_zero(to):
            for id_, value in zip(ids, values):
                self._balance_change(to, id_, value, collection, session)

    def _handle_deal_started(self, deal_index: int, emitter: str, receiver: str, collection: Collection):
        """
        Processes a started deal (metadata will be retrieved and properly updated).
        :param deal_index: The started deal.
        :param emitter: The deal emitter.
        :param receiver: The deal receiver.
        :param collection: The deals' collection.
        """

        # TODO

    def _handle_deal_accepted(self, deal_index: int, collection: Collection):
        """
        Processes an accepted deal (metadata will be retrieved and properly updated).
        :param deal_index: The accepted deal.
        :param collection: The deals' collection.
        """

        # TODO

    def _handle_deal_confirmed(self, deal_index: int, collection: Collection):
        """
        Processes a confirmed deal.
        :param deal_index: The confirmed deal.
        :param collection: The deals' collection.
        """

        # TODO

    def _handle_deal_broken(self, deal_index: int, collection: Collection):
        """
        Processes a broken (rejected, cancelled) deal.
        :param deal_index: The broken deal.
        :param collection: The deals' collection.
        """

        # TODO
