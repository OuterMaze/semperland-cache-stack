from pymongo import MongoClient
from web3.contract import Contract
from .base import MongoDBContractEventHandler


"""
This class has the following requirements in whatever is used as the underlying
database:

1. "sponsoring" collection must be indexed:
   - non-uniquely by `sponsor` (ordering does not matter).
   - non-uniquely by `brand_id` (ordering does not matter).
   - uniquely by the pair (`sponsor`, `brand_id`).
"""


class SponsorRegistryContractEventHandler(MongoDBContractEventHandler):
    """
    This handler stands for the SponsorRegistry contract.
    """

    SPONSORS = "sponsors"

    def __init__(self, contract: Contract, client: MongoClient, db_name: str, session_kwargs: dict):
        super().__init__(contract, client, db_name, session_kwargs)
        self._name = "sponsor-registry"
        self._sponsors = self.db[self.SPONSORS]

    def get_event_names(self):
        """
        Returns the only processed event: Sponsored.
        """

        return ["Sponsored"]

    def process_event(self, event: dict):
        """
        Processes the Sponsored event.
        :param event: The event to process.
        """

        event_name = event['event']
        args = event['args']

        if event_name == "Sponsored":
            sponsor = self._get_arg(args, "sponsor")
            brand_id = self._get_arg(args, "brandId")
            sponsored = self._get_arg(args, "sponsored")
            self._sponsors.replace_one({
                "sponsor": sponsor,
                "brand": brand_id
            }, {
                "sponsor": sponsor,
                "brand": brand_id,
                "sponsored": sponsored
            }, upsert=True, **self.client_session_kwargs)
