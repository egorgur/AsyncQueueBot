from aiogram import Bot
from aiogram.types import CallbackQuery
from core.utils.callbackdata import QueuesButtonInfo, UserIdButtonInfo, UserDeletion, UserAddition, ReturnToQueues, \
    DeleteQueue, RenameQueue, MakeQueue

from core.data_files import funcs

from core.keyboards.inline import get_inline_users_in_queue, get_inline_queues_keyboard


async def select_queue(call: CallbackQuery, bot: Bot, callback_data: QueuesButtonInfo):
    queue_name = callback_data.button_name
    funcs.sort_queue(queue_name)
    queue_list = funcs.read_json('queue_list.json')
    queue = queue_list[queue_name]
    await call.message.delete()
    await call.message.answer('Пользователи',
                              reply_markup=get_inline_users_in_queue(queue, queue_name, str(call.message.from_user.id)))


async def delete_user(call: CallbackQuery, bot: Bot, callback_data: UserDeletion):
    user_id = callback_data.user_id
    queue_name = callback_data.queue_name
    funcs.delete_user_from_queue(user_id, queue_name)
    queue_list = funcs.read_json('queue_list.json')
    queue = queue_list[queue_name]
    await call.message.delete()
    await call.answer('del')
    await call.message.answer('Пользователи',
                              reply_markup=get_inline_users_in_queue(queue, queue_name, str(call.message.from_user.id)))


async def add_user(call: CallbackQuery, bot: Bot, callback_data: UserAddition):
    user_id = callback_data.user_id
    queue_name = callback_data.queue_name
    funcs.add_user_to_last_position_in_queue(user_id, queue_name)
    funcs.sort_queue(queue_name)
    queue_list = funcs.read_json('queue_list.json')
    queue = queue_list[queue_name]
    await call.message.delete()
    await call.answer('add')
    await call.message.answer('Пользователи',
                              reply_markup=get_inline_users_in_queue(queue, queue_name, str(call.message.from_user.id)))


async def show_queues(call: CallbackQuery, bot: Bot, callback_data: ReturnToQueues):
    names = funcs.get_all_queue_names()
    await call.message.delete()
    await call.message.answer(f'все очереди {names}', reply_markup=get_inline_queues_keyboard(names))
