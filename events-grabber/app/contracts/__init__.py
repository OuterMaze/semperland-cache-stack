from web3 import Web3
from web3.providers import HTTPProvider
from .abi import METAVERSE_CONTRACT_ABI, SPONSOR_REGISTRY_CONTRACT_ABI, SIGNATURE_VERIFIER_CONTRACT_ABI, \
    BRAND_REGISTRY_CONTRACT_ABI, ECONOMY_CONTRACT_ABI, CURRENCY_DEFINITION_PLUGIN_CONTRACT_ABI, \
    CURRENCY_MINTING_PLUGIN_CONTRACT_ABI


def get_contracts(http_gateway: str, metaverse_contract_address: str):
    """
    Gets all the contracts
    :param http_gateway: The gateway to use.
    :param metaverse_contract_address: The address of the metaverse contract.
    :return: The list of connected contracts.
    """

    web3client = Web3(HTTPProvider(http_gateway))

    # First, get the metaverse contract.
    metaverse_contract = web3client.eth.contract(
        address=web3client.to_checksum_address(metaverse_contract_address),
        abi=METAVERSE_CONTRACT_ABI
    )

    # Then, get all the other contracts.

    # Sponsoring:
    sponsor_registry_contract_address = metaverse_contract.functions.sponsorRegistry().call()
    sponsor_registry_contract = web3client.eth.contract(
        address=sponsor_registry_contract_address,
        abi=SPONSOR_REGISTRY_CONTRACT_ABI
    )

    # Signature verifier:
    signature_verifier_contract_address = metaverse_contract.functions.signatureVerifier().call()
    signature_verifier_contract = web3client.eth.contract(
        address=signature_verifier_contract_address,
        abi=SIGNATURE_VERIFIER_CONTRACT_ABI
    )

    # Brand registry:
    brand_registry_contract_address = metaverse_contract.functions.brandRegistry().call()
    brand_registry_contract = web3client.eth.contract(
        address=brand_registry_contract_address,
        abi=BRAND_REGISTRY_CONTRACT_ABI
    )

    # Economy:
    economy_contract_address = metaverse_contract.functions.economy().call()
    economy_contract = web3client.eth.contract(
        address=economy_contract_address,
        abi=ECONOMY_CONTRACT_ABI
    )

    # Currency definition plug-in:
    currency_definition_plugin_contract_address = metaverse_contract.functions.pluginsList(0).call()
    currency_definition_plugin_contract = web3client.eth.contract(
        address=currency_definition_plugin_contract_address,
        abi=CURRENCY_DEFINITION_PLUGIN_CONTRACT_ABI
    )

    # Currency minting plug-in:
    currency_minting_plugin_contract_address = metaverse_contract.functions.pluginsList(0).call()
    currency_minting_plugin_contract = web3client.eth.contract(
        address=currency_minting_plugin_contract_address,
        abi=CURRENCY_MINTING_PLUGIN_CONTRACT_ABI
    )

    return {
        "metaverse": metaverse_contract,
        "brand_registry": brand_registry_contract,
        "economy": economy_contract,
        "sponsor_registry": sponsor_registry_contract,
        "signature_verifier": signature_verifier_contract,
        "currency_definition_plugin": currency_definition_plugin_contract,
        "currency_minting_plugin": currency_minting_plugin_contract
    }
