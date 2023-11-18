import binascii
from pymongo import MongoClient
from web3.contract import Contract
from .base import MongoDBContractEventHandler


"""
This class has the following requirements in whatever is used as the underlying
database:

1. "metaverse_permissions" collection must be indexed:
   - non-uniquely by `permission` (ordering does not matter).
   - non-uniquely by `user` (ordering does not matter).
   - uniquely by the pair (`permission`, `user`).
"""


class MetaverseContractEventHandler(MongoDBContractEventHandler):
    """
    This handler stands for the Economy contract.
    """

    METAVERSE_PERMISSIONS = "metaverse_permissions"

    def __init__(self, contract: Contract, client: MongoClient, db_name: str, session_kwargs: dict):
        super().__init__(contract, client, db_name, session_kwargs)
        self._name = "metaverse"
        self._permissions = self.db[self.METAVERSE_PERMISSIONS]

    def get_event_names(self):
        """
        This handler only processes a single event: "PermissionChanged".
        :return: Only the "PermissionChanged" event.
        """

        return ["PermissionChanged"]

    def process_event(self, event: dict):
        """
        Processes the incoming event: PermissionChanged.
        :param event: The event to process.
        """

        event_name = event['event']
        args = event['args']
        if event_name == "PermissionChanged":
            permission = '0x' + binascii.hexlify(self._get_arg(args, 'permission')).decode('utf-8')
            user = self._get_arg(args, 'user')
            set_ = self._get_arg(args, 'set')
            self._permissions.replace_one({"permission": permission, "user": user},
                                          {"permission": permission, "user": user, "value": set_}, upsert=True)
