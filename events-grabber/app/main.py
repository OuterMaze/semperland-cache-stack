import logging
import web3
from pymongo import MongoClient
from pymongo.collection import Collection


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def _tohex(value: int):
    """
    Normalizes an integer value to its hexadecimal representation.
    :param value: The value to normalize to hex.
    :return: The normalized hexadecimal value.
    """

    h = hex(value)[2:]
    return "0x" + ("0" * max(0, 64 - len(h))) + h


def grab_all_events_since(gateway_url: str, contracts_settings: list, state: dict):
    """
    Grabs all the events since a certain limit, per state.
    :param gateway_url: The URL of the gateway to use (it must support event logs retrieval).
    :param contracts_settings: The list with the settings to use.
    :param state: The state (a mapping of eventKey => startBlock) to use.
    :return: A dictionary of blockNumber => events.
    """

    client = web3.Web3(web3.providers.HTTPProvider(gateway_url))
    events_list = {}
    for contract_settings in contracts_settings:
        handler = contract_settings['handler']
        contract_key = handler.contract_key
        contract = client.eth.contract(web3.Web3.toChecksumAddress(contract_settings['address']),
                                       abi=handler.get_abi())
        for event_name in handler.get_events():
            event_state_key = f"{contract_key}:{event_name}"
            event_filter = getattr(contract.events, event_name).createFilter(
                fromBlock=state.get(event_state_key, '0x0')
            )
            for event in event_filter.get_all_entries():
                entry = {**{
                    k: v for k, v in event.items() if k in {"blockNumber", "transactionIndex", "logIndex", "args",
                                                            "event"}
                }, "event-state-key": event_state_key, "contract-key": contract_key}
                events_list.setdefault(entry["blockNumber"], []).append(entry)
    return events_list


def process_full_events_list(events_list: dict, contract_settings: dict, client: MongoClient,
                             state_collection: Collection, state: dict, gateway_url: str):
    """
    Processes all the events in the incoming list. This is done according
    to a given current state (and state collection), its state collection
    (to update it appropriately), and a given client to be used into the
    specific event handlers.
    :param events_list: The list of events to process. This is actually a dictionary.
    :param contract_settings: A dictionary with the per-event settings.
    :param client: A MongoDB client.
    :param state_collection: A collection, related to the client, into which
      the state will be saved.
    :param state: The current state, which is periodically updated and pushed.
    :param gateway_url: The gateway url to create a web3 client.
    :return: The events that were effectively synchronized, and whether an exception
      occurred in the processing.
    """

    all_processed_events = []

    try:
        web3_client = web3.Web3(web3.providers.HTTPProvider(gateway_url))
        with client.start_session() as session:
            # Inside this session, all the events will be iterated.
            # The first iteration level, which will correspond to
            # a MongoDB Transaction, belongs to the block number.
            for blockNumber in sorted(events_list.keys()):
                with session.start_transaction():
                    # Processes all the events. The events themselves
                    # will NOT be stored directly, but the handlers
                    # MAY cause some data be stored.
                    #
                    # Each event is expected to have the following
                    # fields:
                    # - "args" (a dictionary - it contains data that
                    #   might require normalization). To be processed
                    #   by the handlers.
                    # - "blockNumber": An arbitrary-length integer
                    #   number with the block number. If stored, it
                    #   should be normalized (to hex string).
                    # - "transactionIndex": An arbitrary-length integer
                    #   number, but typically -in practice- in the range
                    #   of 32 bits. If stored, in the future it might
                    #   need of normalization (to hex string).
                    # - "logIndex": An arbitrary-length integer number,
                    #   but typically -in practice- in the range of 32
                    #   bits. If stored, in the future it might need of
                    #   normalization (to hex string).
                    # - "eventKey": A unique event key, among the other
                    #   registered events (which are a combination of
                    #   the event address, the ABI, and the name of the
                    #   event we're interested in retrieving).
                    events = sorted(events_list[blockNumber],
                                    key=lambda evt: (evt['transactionIndex'], evt['logIndex']))
                    processed_events = []
                    for event in events:
                        handler = contract_settings[event['contract-key']]["handler"]
                        response = handler(client, session, event, web3_client)
                        if response is not None:
                            processed_events.append(response)
                    # Update and store the states.
                    state[event['event-state-key']] = _tohex(blockNumber + 1)
                    state_collection.replace_one({}, {"value": state}, session=session, upsert=True)
                    # Update response.
                    all_processed_events.extend(processed_events)
        return all_processed_events, None
    except Exception as e:
        LOGGER.exception("Error on processor!")
        return all_processed_events, e


def loop(gateway_url: str, contracts_settings: list, client: MongoClient,
         cache_db: str, cache_state_collection: str):
    """
    The whole work loop, including the state retrieval and the full
      event processing and update. The order is the following: Get
      the current state, if any; retrieve all the events related to
      that state; and process those elements accordingly (block by
      block). Then return all the successfully processed events,
      and whether an error occurred in the middle. The state will
      be consistently stored.
    :param gateway_url: The URL of the gateway to use (it must support
      event logs retrieval).
    :param contracts_settings: The dictionary with the settings to use.
    :param client: A MongoDB client.
    :param cache_db: The db that will be related to this cache feature.
    :param cache_state_collection: The collection, inside the db
      used as cache, that will hold the current state.
    :return: A list of successfully processed events, and whether
      an error occurred or not in that processing.
    """

    state_collection = client[cache_db][cache_state_collection]
    state = (state_collection.find_one({}) or {}).get('value', {})
    LOGGER.info(f"loop::Using state: {state} against gateway: {gateway_url}")
    events_list = grab_all_events_since(gateway_url, contracts_settings, state)
    LOGGER.info(f"loop::Processing events ({len(events_list)})")
    return process_full_events_list(events_list, {cs['handler'].contract_key: cs for cs in contracts_settings},
                                    client, state_collection, state, gateway_url)


if __name__ == "__main__":
    # Implement the grabber here.
    pass
