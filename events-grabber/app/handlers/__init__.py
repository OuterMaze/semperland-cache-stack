from pymongo import MongoClient
from pymongo.client_session import ClientSession
from web3.contract import Contract
from .base import ContractEventHandlers
from .metaverse import MetaverseContractEventHandler
from .brand_registry import BrandRegistryContractEventHandler
from .currency_definition_plugin import CurrencyDefinitionPluginContractEventHandler
from .currency_minting_plugin import CurrencyMintingPluginContractEventHandler
from .economy import EconomyContractEventHandler
from .sponsor_registry import SponsorRegistryContractEventHandler


def make_handlers(client: MongoClient, db_name: str, session_kwargs: dict,
                  metaverse_contract: Contract, brand_registry_contract: Contract,
                  economy_contract: Contract, sponsor_registry_contract: Contract,
                  currency_definition_plugin_contract: Contract,
                  currency_minting_plugin_contract: Contract) -> ContractEventHandlers:
    """
    Makes a set of contract handlers.
    :param client: The MongoDB client.
    :param db_name: The database name.
    :param session_kwargs: The -optionally- MongoDB session.
    :param metaverse_contract: The metaverse contract.
    :param brand_registry_contract: The brand registry contract.
    :param economy_contract: The economy contract.
    :param sponsor_registry_contract: The sponsor registry contract.
    :param currency_definition_plugin_contract: The currency definition plug-in contract.
    :param currency_minting_plugin_contract: The currency minting plug-in contract.
    :return: The set of contract handlers.
    """

    return ContractEventHandlers(
        MetaverseContractEventHandler(metaverse_contract, client, db_name, session_kwargs),
        EconomyContractEventHandler(economy_contract, client, db_name, session_kwargs),
        BrandRegistryContractEventHandler(brand_registry_contract, metaverse_contract,
                                          client, db_name, session_kwargs),
        SponsorRegistryContractEventHandler(sponsor_registry_contract, client, db_name, session_kwargs),
        CurrencyDefinitionPluginContractEventHandler(currency_definition_plugin_contract, metaverse_contract,
                                                     client, db_name, session_kwargs),
        CurrencyMintingPluginContractEventHandler(currency_minting_plugin_contract, metaverse_contract,
                                                  client, db_name, session_kwargs)
    )
