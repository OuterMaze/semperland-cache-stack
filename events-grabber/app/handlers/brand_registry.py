import binascii
import logging
from pymongo import MongoClient
from web3.contract import Contract
from .base import MetaverseRelatedContractEventHandler


"""
This class has the following requirements in whatever is used as the underlying
database:

1. "brand_permissions" collection must be indexed:
   - non-uniquely by `brand_id` (ordering does not matter.)
   - non-uniquely by (`brand_id`, `permission`) (ordering does not matter).
   - non-uniquely by `user` (ordering does not matter).
   - uniquely by the pair (`brand_id`, `permission`, `user`).
"""


LOGGER = logging.getLogger("BRAND_REGISTRY")
LOGGER.setLevel(logging.INFO)


class BrandRegistryContractEventHandler(MetaverseRelatedContractEventHandler):
    """
    This handler stands for the BrandRegistry contract.
    """

    BRAND_PERMISSIONS = "brand_permissions"

    def __init__(self, contract: Contract, metaverse_contract: Contract,
                 client: MongoClient, db_name: str, session_kwargs: dict):
        super().__init__(contract, metaverse_contract, client, db_name, session_kwargs)
        self._name = "brand-registry"
        self._permissions = self.db[self.BRAND_PERMISSIONS]

    def get_event_names(self):
        """
        This handler processes the Brand-related events.
        :return: The handler for the Brand-related events.
        """

        return ["BrandRegistrationCostUpdated", "BrandRegistered", "BrandUpdated",
                "BrandSocialCommitmentUpdated", "BrandPermissionChanged"]

    def process_event(self, event: dict):
        """
        Processes the brand-related events.
        :param event: The event to process.
        """

        event_name = event['event']
        args = event['args']

        if event_name == "BrandRegistrationCostUpdated":
            self._set_parameter("brand_registration_cost", str(self._get_arg(args, "newCost")))
        elif event_name == "BrandRegistered":
            self._download_metadata(int(self._get_arg(args, "brandId"), 16), "brand")
        elif event_name == "BrandUpdated" or event_name == "BrandSocialCommitmentUpdated":
            LOGGER.info(f"BrandRegistry event: {event_name}, args: {args}")
            self._download_metadata(int(self._get_arg(args, "brandId")), "brand")
        elif event_name == "BrandPermissionChanged":
            brand_id = self._get_arg(args, "brandId")
            permission = '0x' + binascii.hexlify(self._get_arg(args, 'permission')).decode('utf-8')
            user = self._get_arg(args, "user")
            set_ = self._get_arg(args, "set")
            self._permissions.replace_one({"permission": permission, "user": user, "brand_id": brand_id},
                                          {"permission": permission, "user": user, "brand_id": brand_id,
                                           "value": set_}, upsert=True)
