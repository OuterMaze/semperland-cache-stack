from .base import MetaverseRelatedContractEventHandler


class CurrencyMintingPluginContractEventHandler(MetaverseRelatedContractEventHandler):
    """
    This handler stands for the CurrencyMintingPlugin contract.
    """

    def get_event_names(self):
        """
        Returns the list of events for parameter change.
        :return: The list of supported events.
        """

        return ["CurrencyMintCostUpdated", "CurrencyMintAmountUpdated"]

    def process_event(self, event: dict):
        """
        Processes the cost/amount update event.
        :param event: The event being processed.
        """

        event_name = event['event']
        args = event['args']

        if event_name == "CurrencyMintCostUpdated":
            self._set_parameter("currency_minting_cost", str(self._get_arg(args, "newCost")))
        elif event_name == "CurrencyMintAmountUpdated":
            self._set_parameter("currency_minting_amount", str(self._get_arg(args, "newAmount")))
