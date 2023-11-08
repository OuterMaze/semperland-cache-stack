from typing import List
from pymongo import MongoClient, ASCENDING
from pymongo.collection import Collection
from ..handlers.base import MetaverseRelatedContractEventHandler
from ..handlers import BrandRegistryContractEventHandler, EconomyContractEventHandler, \
    MetaverseContractEventHandler, SponsorRegistryContractEventHandler


def _make_index(collection: Collection, index_name: str, unique: bool, fields: List[tuple]):
    """
    Makes an index for a given collection.
    :param collection: The collection.
    :param index_name: The index name.
    :param unique: Whether the index is unique.
    :param fields: The list of fields.
    """

    try:
        collection.create_index(fields, name=index_name, unique=unique,
                                background=False, sparse=True)
    except:
        pass


def _make_indices(client: MongoClient, db_name: str):
    """
    Makes all the needed indices into the DB.
    :param client: The MongoDB client.
    :param db_name: The database name.
    """

    db = client[db_name]

    # Indices for metaverse permissions.
    metaverse_permissions = db[MetaverseContractEventHandler.METAVERSE_PERMISSIONS]
    _make_index(metaverse_permissions, "for_permission", False, [("permission", ASCENDING)])
    _make_index(metaverse_permissions, "for_user", False, [("user", ASCENDING)])
    _make_index(metaverse_permissions, "full_match", True,
                [("permission", ASCENDING), ("user", ASCENDING)])

    # Indices for tokens metadata.
    tokens_metadata = db[MetaverseRelatedContractEventHandler.TOKENS_METADATA]
    _make_index(tokens_metadata, "for_token_id", True, [("token_id", ASCENDING)])
    _make_index(tokens_metadata, "for_brand_id", False, [("brand_id", ASCENDING)])
    _make_index(tokens_metadata, "for_token_type", False, [("token_type", ASCENDING)])

    # Indices for brand permission.
    brand_permissions = db[BrandRegistryContractEventHandler.BRAND_PERMISSIONS]
    _make_index(brand_permissions, "for_brand_id", False,
                [("brand_id", ASCENDING)])
    _make_index(brand_permissions, "for_brand_id_and_permission", False,
                [("brand_id", ASCENDING), ("permission", ASCENDING)])
    _make_index(brand_permissions, "for_user", False,
                [("user", ASCENDING)])
    _make_index(brand_permissions, "full_match", True,
                [("brand_id", ASCENDING), ("permission", ASCENDING), ("user", ASCENDING)])

    # Indices for deals.
    deals = db[EconomyContractEventHandler.DEALS]
    _make_index(deals, "for_index", True, [("index", ASCENDING)])
    _make_index(deals, "for_emitter", False, [("emitter", ASCENDING)])
    _make_index(deals, "for_receiver", False, [("receiver", ASCENDING)])

    # Indices for balances.
    balances = db[EconomyContractEventHandler.BALANCES]
    _make_index(balances, "for_token", False, [("token", ASCENDING)])
    _make_index(balances, "for_owner", False, [("owner", ASCENDING)])
    _make_index(balances, "full_match", True, [("token", ASCENDING), ("owner", ASCENDING)])

    # Indices for sponsors.
    sponsors = db[SponsorRegistryContractEventHandler.SPONSORS]
    _make_index(balances, "for_sponsor", False, [("sponsor", ASCENDING)])
    _make_index(balances, "for_brand_id", False, [("brand_id", ASCENDING)])
    _make_index(balances, "full_match", True,
                [("sponsor", ASCENDING), ("brand_id", ASCENDING)])
