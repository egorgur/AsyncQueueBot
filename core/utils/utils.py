from dataclasses import dataclass


@dataclass
class UtilData:
    last_bot_message_id: dict
    queue_name: str
    last_action: dict
    swap_requests: dict


util_data = UtilData(last_bot_message_id={}, queue_name='', last_action={}, swap_requests={})
