from dataclasses import dataclass


@dataclass
class UtilData:
    last_bot_message_id: int
    queue_name: str
    user_id: int


util_data = UtilData(last_bot_message_id=-1, queue_name='', user_id=-1)
