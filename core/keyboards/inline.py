from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.callbackdata import QueuesButtonInfo

select_mackbook = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='inl 1',
            callback_data='inl1_data'
        ),
        InlineKeyboardButton(
            text='inl 2',
            callback_data='inl2_data'
        )
    ],
    [
        InlineKeyboardButton(
            text='inl 3',
            callback_data='inl3_data'
        ),
        InlineKeyboardButton(
            text='link',
            url='https://vk.com/dungeon_enjoyer'
        )
    ]
])


def get_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    for i in range(5):
        keyboard_builder.button(text=f'кнопка номер {i}',
                                callback_data=QueuesButtonInfo(button_name=f'{i}'))

    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()


def get_inline_queues_keyboard(queue_names):
    keyboard_builder = InlineKeyboardBuilder()
    for i in queue_names:
        keyboard_builder.button(text=f'{i}',
                                callback_data=QueuesButtonInfo(button_name=f'{i}'))