from typing import List
from pymongo import MongoClient
from pymongo.client_session import ClientSession
from web3.contract import Contract
from .base import MongoDBContractEventHandler


"""
This class has the following requirements in whatever is used as the underlying
database:

1. "deals" collection must be indexed:
   - uniquely by `index`.
   - non-uniquely by `emitter` (ordering does not matter).
   - non-uniquely by `receiver` (ordering does not matter).

2. "balances" collection must be indexed:
   - non-uniquely by `token` (ordering does not matter).
   - non-uniquely by `owner` (ordering does not matter).
   - uniquely by the pair (`token`, `owner`).
"""


class EconomyContractHandler(MongoDBContractEventHandler):
    """
    This handler stands for the Economy contract.
    """

    DEALS = "deals"
    BALANCES = "balances"

    def __init__(self, contract: Contract, client: MongoClient, db_name: str, session: ClientSession):
        super().__init__(contract, client, db_name, session)
        self._deals = self.db[self.DEALS]
        self._balances = self.db[self.BALANCES]

    def get_event_names(self):
        """
        This handler processes 6 events: Transfer-related and deal-related.
        :return: The names of the 6 events.
        """

        return ["TransferSingle", "TransferBatch", "DealStarted", "DealAccepted",
                "DealConfirmed", "DealBroken"]

    def process_event(self, event: dict):
        """
        Processes two types of events: TransferSingle/Batch, and
        DealStarted/Accepted/Confirmed/Broken. The Data is stored
        into two different collections.
        :param event: The event to process.
        """

        event_name = event['event']
        args = event['args']
        from_ = self._get_arg(args, 'from')
        to = self._get_arg(args, 'to')

        if event_name == 'TransferSingle':
            id_ = hex(self._get_arg(args, 'id') or 0)
            value = self._get_arg(args, 'value') or 0
            self._handle_transfer_single(from_, to, id_, value)
        elif event_name == 'TransferBatch':
            ids_ = [hex(k) for k in self._get_arg(args, 'ids') or []]
            values = self._get_arg(args, 'values') or []
            self._handle_transfer_batch(from_, to, ids_, values)
        elif event_name == 'DealStarted':
            self._handle_deal_started(self._get_arg(args, 'dealId'),
                                      self._get_arg(args, 'emitter'),
                                      self._get_arg(args, 'receiver'))
        elif event_name == 'DealAccepted':
            self._handle_deal_accepted(self._get_arg(args, 'dealId'))
        elif event_name == 'DealConfirmed':
            self._handle_deal_confirmed(self._get_arg(args, 'dealId'))
        elif event_name == 'DealBroken':
            self._handle_deal_broken(self._get_arg(args, 'dealId'))

    def _balance_change(self, from_: str, id_: str, value: int):
        """
        Decrements the balance of a given (owner, token) entry.
        :param from_: The owner.
        :param id_: The token id.
        """

        from_entry = self._balances.find_one({
            "owner": from_,
            "token": id_
        }, session=self._session) or {}
        from_balance = int(from_entry.get('amount') or '0')
        from_balance += value
        from_balance_str = str(from_balance)
        self._balances.replace_one({
            "owner": from_,
            "token": id_
        }, {
            "owner": from_,
            "token": id_,
            "amount": from_balance_str
        }, session=self._session, upsert=True)

    def _handle_transfer_single(self, from_: str, to: str, id_: str, value: int):
        """
        Processes a TransferSingle event, in a similar way to how ERC-20 processes
        its Transfer event, but also telling the token id.
        :param from_: The token sender. It will be zero on mint.
        :param to: The token receiver. It will be zero on burn.
        :param id_: The token id.
        :param value: The token amount.
        """

        if not self._is_zero(from_):
            self._balance_change(from_, id_, -value)
        if not self._is_zero(to):
            self._balance_change(to, id_, value)

    def _handle_transfer_batch(self, from_: str, to: str, ids: List[str], values: List[int]):
        """
        Processes a TransferBatch event, which involves per-token updates.
        :param from_: The token sender. It will be zero on mint.
        :param to: The token receiver. It will be zero on burn.
        :param ids: The token ids.
        :param values: The respective token amounts.
        """

        if not self._is_zero(from_):
            for id_, value in zip(ids, values):
                self._balance_change(from_, id_, -value)
        if not self._is_zero(to):
            for id_, value in zip(ids, values):
                self._balance_change(to, id_, value)

    def _handle_deal_started(self, deal_index: int, emitter: str, receiver: str):
        """
        Processes a started deal (metadata will be retrieved and properly updated).
        :param deal_index: The started deal.
        :param emitter: The deal emitter.
        :param receiver: The deal receiver.
        """

        emitter_ids, emitter_amounts, _, _ = self.contract.functions.dealsContents(deal_index)
        self._deals.insert_one({
            "index": deal_index,
            "emitter": emitter,
            "receiver": receiver,
            "emitter_ids": emitter_ids,
            "emitter_amounts": emitter_amounts,
            "status": "created"
        }, session=self.client_session)

    def _handle_deal_accepted(self, deal_index: int):
        """
        Processes an accepted deal (metadata will be retrieved and properly updated).
        :param deal_index: The accepted deal.
        """

        _, _, receiver_ids, receiver_amounts = self.contract.functions.dealsContents(deal_index)
        self._deals.update_one({
            "index": deal_index
        }, {"$set": {
            "receiver_ids": receiver_ids,
            "receiver_amounts": receiver_amounts,
            "status": "accepted"
        }}, session=self.client_session)

    def _handle_deal_confirmed(self, deal_index: int):
        """
        Processes a confirmed deal. By this event, the deal is REMOVED
        from the blockchain, but will be kept in the cache.
        :param deal_index: The confirmed deal.
        """

        self._deals.update_one({
            "index": deal_index
        }, {"$set": {
            "status": "confirmed"
        }}, session=self.client_session)

    def _handle_deal_broken(self, deal_index: int):
        """
        Processes a broken (rejected, cancelled) deal. By this event,
        the deal is REMOVED from the blockchain, but will be kept in
        the cache.
        :param deal_index: The broken deal.
        """

        self._deals.update_one({
            "index": deal_index
        }, {"$set": {
            "status": "rejected"
        }}, session=self.client_session)
