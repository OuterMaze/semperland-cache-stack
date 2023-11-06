from web3 import Web3
from web3.providers import HTTPProvider


def get_contracts(http_gateway: str, metaverse_contract_address: str):
    """
    Gets all the contracts
    :param http_gateway: The gateway to use.
    :param metaverse_contract_address: The address of the metaverse contract.
    :return: The list of connected contracts.
    """

