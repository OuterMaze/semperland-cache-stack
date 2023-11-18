from .base import MetaverseRelatedContractEventHandler


class CurrencyDefinitionPluginContractEventHandler(MetaverseRelatedContractEventHandler):
    """
    This handler stands for the CurrencyDefinitionPlugin contract.
    """

    def get_event_names(self):
        """
        Returns the list of events: for parameter change, metadata
          update, and first definition.
        :return: The list of supported events.
        """

        return ["CurrencyDefinitionCostUpdated", "CurrencyDefined", "CurrencyMetadataUpdated"]

    def process_event(self, event: dict):
        """
        Processes one of the events: definition, update or definition-cost update.
        :param event: The event to process.
        """

        event_name = event['event']
        args = event['args']

        if event_name == "CurrencyDefinitionCostUpdated":
            self._set_parameter("currency_definition_cost", str(self._get_arg(args, "newCost")))
        elif event_name == "CurrencyDefined":
            self._download_metadata(self._get_arg(args, "tokenId"), "currency")
        elif event_name == "CurrencyMetadataUpdated":
            self._download_metadata(self._get_arg(args, "tokenId"), "currency")
