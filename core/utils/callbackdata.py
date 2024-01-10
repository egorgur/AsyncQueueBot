from aiogram.filters.callback_data import CallbackData


class QueuesButtonInfo(CallbackData, prefix='queues_'):
    button_name: str
