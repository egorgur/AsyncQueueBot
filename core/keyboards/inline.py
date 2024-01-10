from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.callbackdata import QueuesButtonInfo, NoneInfo, UserDeletion, UserAddition, ReturnToQueues, RenameQueue, \
    DeleteQueue, MakeQueue

select = InlineKeyboardMarkup(inline_keyboard=[
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


def get_inline_queues_control(queue_names: list):
    keyboard_builder = InlineKeyboardBuilder()
    for i in range(len(queue_names)):
        keyboard_builder.button(text=f'{queue_names[i]}',
                                callback_data=NoneInfo())
        keyboard_builder.button(text='Переименовать',
                                callback_data=RenameQueue(queue_name=queue_names[i]))
        keyboard_builder.button(text='Удалить',
                                callback_data=DeleteQueue(queue_name=queue_names[i]))
    keyboard_builder.button(text='Создать очередь',
                            callback_data=MakeQueue())
    keyboard_builder.adjust(3, repeat=True)
    return keyboard_builder.as_markup()


def get_inline_queues_keyboard(queue_names: list):
    keyboard_builder = InlineKeyboardBuilder()
    for i in queue_names:
        keyboard_builder.button(text=f'{i}',
                                callback_data=QueuesButtonInfo(button_name=f'{i}'))
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()


def get_inline_users_in_queue(queue: dict, queue_name: str, user_id_that_calls: str):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Назад к очередям',
                            callback_data=ReturnToQueues())
    for i in range(len(queue)):
        keyboard_builder.button(text=f'{list(queue.keys())[i]} {list(queue.values())[i]}',
                                callback_data=QueuesButtonInfo(button_name=list(queue.values())[i]))
    if user_id_that_calls in queue.values():
        keyboard_builder.button(text='Удалиться',
                                callback_data=UserDeletion(user_id=user_id_that_calls, queue_name=queue_name))
    else:
        keyboard_builder.button(text='Добавиться',
                                callback_data=UserAddition(user_id=user_id_that_calls, queue_name=queue_name))
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
