from aiogram import types, Bot
from aiogram.types import CallbackQuery
from asyncio import sleep

from core.utils.callbackdata import QueuesButtonInfo, UserIdButtonInfo, UserDeletion, UserAddition, ReturnToQueues, \
    DeleteQueue, RenameQueue, MakeQueue, SpecUserAdditionCall, SpecUserAddition, UserToSwap

from core.data_files import funcs

from core.keyboards.inline import get_inline_users_in_queue, get_inline_queues_keyboard, get_inline_queues_control, \
    empty_positions

from core.utils.utils import util_data


async def select_queue(call: CallbackQuery, bot: Bot, callback_data: QueuesButtonInfo):
    queue_name = callback_data.button_name
    funcs.sort_queue(queue_name)
    queue_list = funcs.read_json('queue_list.json')
    queue = queue_list[queue_name]
    await call.message.delete()
    await call.message.answer(f'Очередь {queue_name}',
                              reply_markup=get_inline_users_in_queue(queue, queue_name, str(call.from_user.id)))


async def delete_user(call: CallbackQuery, bot: Bot, callback_data: UserDeletion):
    user_id = callback_data.user_id
    queue_name = callback_data.queue_name
    position = funcs.get_user_pos(user_id, queue_name)
    funcs.delete_user_from_queue(user_id, queue_name)
    funcs.update_positions(queue_name, position)
    queue_list = funcs.read_json('queue_list.json')
    queue = queue_list[queue_name]
    await call.message.delete()
    await call.message.answer(f'Очередь {queue_name}',
                              reply_markup=get_inline_users_in_queue(queue, queue_name, str(call.from_user.id)))


async def add_user(call: CallbackQuery, bot: Bot, callback_data: UserAddition):
    user_id = callback_data.user_id
    queue_name = callback_data.queue_name
    funcs.add_user_to_last_position_in_queue(user_id, queue_name)
    funcs.sort_queue(queue_name)
    queue_list = funcs.read_json('queue_list.json')
    queue = queue_list[queue_name]
    await call.message.delete()
    await call.message.answer(f'Очередь {queue_name}',
                              reply_markup=get_inline_users_in_queue(queue, queue_name, str(call.from_user.id)))


async def delete_queue(call: CallbackQuery, bot: Bot, callback_data: DeleteQueue):
    queue_name = callback_data.queue_name
    funcs.delete_queue(queue_name)
    names = funcs.get_all_queue_names()
    await call.message.delete()
    await call.message.answer(f'все очереди {names}', reply_markup=get_inline_queues_control(names))


async def show_queues(call: CallbackQuery, bot: Bot, callback_data: ReturnToQueues):
    names = funcs.get_all_queue_names()
    await call.message.delete()
    await call.message.answer(f'все очереди {names}', reply_markup=get_inline_queues_keyboard(names))


async def rename_queue_call(call: CallbackQuery, bot: Bot, callback_data: RenameQueue):
    queue_name = callback_data.queue_name
    util_data.queue_name = queue_name
    util_data.last_bot_message_id[call.from_user.id] = call.message.message_id
    util_data.last_action[call.from_user.id] = 'rename'
    await call.message.delete()
    await call.message.answer(f'Переименовать {queue_name}. Напишите новое название реплаем на это сообщение')


async def make_queue_call(call: CallbackQuery, bot: Bot, callback_data: MakeQueue):
    util_data.last_bot_message_id[call.from_user.id] = call.message.message_id
    util_data.last_action[call.from_user.id] = 'make'
    await call.message.delete()
    await call.message.answer(f'Напишите название новой очереди реплаем на это сообщение')


async def spec_user_add_menu(call: CallbackQuery, bot: Bot, callback_data: SpecUserAdditionCall):
    user_id = callback_data.user_id
    queue_name = callback_data.queue_name
    queue_list = funcs.read_json('queue_list.json')
    queue = queue_list[queue_name]
    await call.message.delete()
    await call.message.answer(f'Выберите незанятое место',
                              reply_markup=empty_positions(queue=queue, queue_name=queue_name,
                                                           user_id_that_calls=user_id))


async def spec_user_add(call: CallbackQuery, bot: Bot, callback_data: SpecUserAddition):
    user_id = callback_data.user_id
    queue_name = callback_data.queue_name
    position = callback_data.position
    queue_list = funcs.read_json('queue_list.json')
    queue = queue_list[queue_name]
    funcs.add_user_to_specific_position_in_queue(user_id, position, queue_name)
    funcs.sort_queue(queue_name)
    queue_list = funcs.read_json('queue_list.json')
    queue = queue_list[queue_name]
    await call.message.delete()
    await call.message.answer('Пользователи',
                              reply_markup=get_inline_users_in_queue(queue, queue_name, str(call.from_user.id)))


async def user_swap_request_registrator(call: CallbackQuery, bot: Bot, callback_data: UserToSwap):
    user_1_id = callback_data.user_1_id
    user_2_id = callback_data.user_2_id
    queue_name = callback_data.queue_name
    user_1_pos = funcs.get_user_pos(callback_data.user_1_id, queue_name)
    user_2_pos = funcs.get_user_pos(callback_data.user_2_id, queue_name)
    if user_1_pos == 'No_user_in_queue':
        await call.message.answer('Пока вас нет в очереди вы не можете отправлять запрос на смену мест')
        return 0
    user_1_msg = await call.message.answer(text=f'Вы отправили запрос {funcs.get_user_name_by_id(user_2_id)}')

    user_2_msg = await bot.send_message(
        text=f'{funcs.get_user_name_by_id(user_1_id)} отправил вам запрос на смену мест в очереди {queue_name}\n'
             f'Ваше место: {user_2_pos}\n'
             f'Место {funcs.get_user_name_by_id(user_1_id)}: {user_1_pos}\n'
             f'Запрос действителен 30 секунд. Принять запрос /swap', chat_id=user_2_id)

    util_data.swap_requests[user_1_id + '->' + user_2_id] = {'message_from': user_1_msg, 'message_to': user_2_msg,
                                                             'queue_name': queue_name}
    for i in range(1, 30):
        await sleep(1)
        await user_2_msg.edit_text(
            text=f'{funcs.get_user_name_by_id(user_1_id)} отправил вам запрос на смену мест в очереди {queue_name}\n'
                 f'Ваше место: {user_2_pos}\n'
                 f'Место {funcs.get_user_name_by_id(user_1_id)}: {user_1_pos}\n'
                 f'Запрос действителен {30 - i} секунд. Принять запрос /swap')
        if not (user_1_id + '->' + user_2_id) in util_data.swap_requests.keys():
            await bot.delete_message(chat_id=user_1_msg.chat.id, message_id=user_1_msg.message_id)
            await bot.delete_message(chat_id=user_2_msg.chat.id, message_id=user_2_msg.message_id)
            return 0
    util_data.swap_requests.pop(user_1_id + '->' + user_2_id)
    await bot.delete_message(chat_id=user_1_msg.chat.id, message_id=user_1_msg.message_id)
    await bot.delete_message(chat_id=user_2_msg.chat.id, message_id=user_2_msg.message_id)
