from dataclasses import dataclass


@dataclass
class UtilData:
    last_bot_message_id: dict
    queue_name: dict
    last_action: dict
    swap_requests: dict
    time_for_queue: str


util_data = UtilData(last_bot_message_id={}, queue_name={}, last_action={}, swap_requests={}, time_for_queue='')
