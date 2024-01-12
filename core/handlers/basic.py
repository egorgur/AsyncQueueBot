from aiogram import types, Bot

from core.data_files import funcs

from core.keyboards.reply import reply_keyboard

from core.keyboards.inline import get_inline_queues_control, get_inline_queues_keyboard, get_inline_users_in_queue
from core.utils.utils import util_data


async def start_command(message: types.Message, bot: Bot):
    funcs.add_user_to_registered_users(dict(message.from_user), str(message.from_user.id))
    await message.answer(f'Привет {message.from_user.first_name}. Это бот для работы с очередями',
                         reply_markup=reply_keyboard)


async def view_all_queues(message: types.Message, bot: Bot):
    names = funcs.get_all_queue_names()
    await message.answer(f'все очереди {names}', reply_markup=get_inline_queues_keyboard(names))


async def view_queues_control_menu(message: types.Message, bot: Bot):
    names = funcs.get_all_queue_names()
    print(names)
    await message.answer(f'все очереди {names}', reply_markup=get_inline_queues_control(names))


async def get_photo(message: types.Message, bot: Bot):
    await message.answer('картинка')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, 'downloads/photo.png')


async def reply_processing(message: types.Message, bot: Bot):
    await message.answer(f'{message.reply_to_message.message_id}, {util_data.last_bot_message_id[message.from_user.id]}')
    if message.reply_to_message.message_id == util_data.last_bot_message_id[message.from_user.id] + 1:
        if not message.text:
            await message.answer('Неверный ввод')
            return 0
        if len(message.text) >= 20:
            await message.answer('Слишком длинное название')
            return 0
        alphabet=("1234567890"
                  "abcdefghijklmnopqrstuvwxyz"
                  "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                  "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
                  "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
                  " ")
        if [symbol for symbol in message.text if symbol not in alphabet]:
            await message.answer('Запрещённые символы')
            return 0
        if util_data.last_action[message.from_user.id] == 'make':
            funcs.make_new_queue(message.text)
            funcs.add_user_to_last_position_in_queue(str(message.from_user.id), message.text)
            await message.answer('Очередь создана')
        elif util_data.last_action[message.from_user.id] == 'rename':
            funcs.rename_queue(util_data.queue_name, message.text)
            await message.answer('Очередь переименована')


async def accepting_swap_request(message: types.Message, bot: Bot):
    if funcs.find_last_swap_call(util_data.swap_requests, str(message.from_user.id)) == 'no_swap_requests':
        await message.answer('Нет запросов на смену мест')
        return 0
    swap_request = util_data.swap_requests[
        funcs.find_last_swap_call(util_data.swap_requests, str(message.from_user.id))]
    util_data.swap_requests.pop(funcs.find_last_swap_call(util_data.swap_requests, str(message.from_user.id)))
    funcs.swap_positions(str(swap_request['message_from'].chat.id), str(swap_request['message_to'].chat.id),
                         swap_request['queue_name'])
    await message.answer(
        f'Вы поменялись местом с {funcs.get_user_name_by_id(str(swap_request['message_from'].chat.id))}')
    await message.answer(f'Очередь {swap_request['queue_name']}',
                         reply_markup=get_inline_users_in_queue(funcs.get_queue(swap_request['queue_name']),
                                                                swap_request['queue_name'],
                                                                str(swap_request['message_to'].chat.id)))
    await bot.send_message(chat_id=swap_request['message_from'].chat.id,
                           text=f'Вы поменялись местом с {funcs.get_user_name_by_id(str(swap_request['message_to'].chat.id))}')
    await bot.send_message(chat_id=swap_request['message_from'].chat.id, text=f'Очередь {swap_request['queue_name']}',
                           reply_markup=get_inline_users_in_queue(funcs.get_queue(swap_request['queue_name']),
                                                                  swap_request['queue_name'],
                                                                  str(swap_request['message_to'].chat.id)))
