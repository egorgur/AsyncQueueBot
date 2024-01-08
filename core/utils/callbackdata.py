from aiogram.filters.callback_data import CallbackData


class ButtonInfo(CallbackData, prefix='button_callback_data'):
    button_name: str
    button_data: str
