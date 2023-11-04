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
