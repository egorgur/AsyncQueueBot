import logging

from aiogram import types, Bot
from aiogram import exceptions

from asyncio import sleep

from data_files import funcs

from keyboards.reply import reply_keyboard

from settings import ADMIN_ID

from keyboards.inline import get_inline_queues_control, get_inline_queues_keyboard, get_inline_users_in_queue, \
    get_inline_timed_queues_control
from utils.utils import util_data


async def start_command(message: types.Message, bot: Bot):
    funcs.add_user_to_registered_users(dict(message.from_user), str(message.from_user.id))
    await message.answer(f'Привет {message.from_user.first_name}. Это бот для работы с очередями',
                         reply_markup=reply_keyboard)


async def view_all_queues(message: types.Message, bot: Bot):
    names = funcs.get_all_queue_names()
    await message.answer(f'Все очереди', reply_markup=get_inline_queues_keyboard(names))


async def view_queues_control_menu(message: types.Message, bot: Bot):
    if message.from_user.id in ADMIN_ID:
        names = funcs.get_all_queue_names()
        await message.answer(f'Все очереди', reply_markup=get_inline_queues_control(names))
    else:
        await message.answer('Вы не админ')


async def get_photo(message: types.Message, bot: Bot):
    await message.answer('картинка')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, 'downloads/photo.png')


async def reply_processing(message: types.Message, bot: Bot):
    try:
        if message.reply_to_message.message_id == util_data.last_bot_message_id[message.from_user.id].message_id:
            if not message.text:
                await message.answer('Неверный ввод')
                return 0
            alphabet = ("1234567890"
                        "abcdefghijklmnopqrstuvwxyz"
                        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                        "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
                        "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
                        ",.() ")
            if [symbol for symbol in message.text if symbol not in alphabet]:
                await message.answer('Запрещённые символы')
                return 0
            if util_data.last_action[message.from_user.id] == 'make_timed':
                try:
                    name = message.text.split(')')[0]
                    name = name.replace('(', '')
                    date, time = message.text.split(')')[1].split(' ')[1], message.text.split(')')[1].split(' ')[2]
                    if not name:
                        await message.answer('Неверный ввод названия')
                        return 0
                    if len(name)>19:
                        await message.answer('Название слишком длинное')
                        return 0
                    if len(date) > 2:
                        await message.answer('Неверный ввод даты')
                        return 0
                    if len(time) < 4 or ('.' not in time) or len(time) > 5:
                        await message.answer('Неверный ввод времени')
                        return 0
                    if len(time) == 4:
                        time = '0' + time
                    funcs.make_timed_queue(name, date, time)
                    queue_data = funcs.get_all_timed_queue_data()
                    await message.answer(f'Отложенные очереди',
                                         reply_markup=get_inline_timed_queues_control(queue_data))
                    return 0
                except:
                    await message.answer('Неверный ввод данных очереди')
                    return 0
            if len(message.text) >= 20:
                await message.answer('Слишком длинное название')
                return 0
            if util_data.last_action[message.from_user.id] == 'make':
                funcs.make_new_queue(str(message.text))
                funcs.add_user_to_last_position_in_queue(str(message.from_user.id), str(message.text))
                await ping_all_users(bot, f'Создана очередь {message.text}')
                await message.answer('Очередь создана',
                                     reply_markup=reply_keyboard)
            elif util_data.last_action[message.from_user.id] == 'rename':
                funcs.rename_queue(util_data.queue_name[message.from_user.id], str(message.text))
                await message.answer('Очередь переименована',
                                     reply_markup=reply_keyboard)
    except KeyError:
        logging.error(f"From [ID:{message.from_user.id}]:Key Error, Call to old message")


async def cancel_swap_request(message: types.Message, bot: Bot):
    if funcs.find_first_swap_call(util_data.swap_requests, str(message.from_user.id)) == 'no_swap_requests':
        await message.answer('Не отправляли запросов на смену')
        return 0
    swap_request = util_data.swap_requests[
        funcs.find_first_swap_call(util_data.swap_requests, str(message.from_user.id))]
    util_data.swap_requests.pop(funcs.find_first_swap_call(util_data.swap_requests, str(message.from_user.id)))
    await message.answer(
        f"Вы отменили запрос к {funcs.get_user_name_by_id(str(swap_request['message_to'].chat.id))}")


async def deni_swap_request(message: types.Message, bot: Bot):
    if funcs.find_last_swap_call(util_data.swap_requests, str(message.from_user.id)) == 'no_swap_requests':
        await message.answer('Нет запросов на смену мест')
        return 0
    swap_request = util_data.swap_requests[
        funcs.find_last_swap_call(util_data.swap_requests, str(message.from_user.id))]
    util_data.swap_requests.pop(funcs.find_last_swap_call(util_data.swap_requests, str(message.from_user.id)))
    await message.answer(
        f"Вы отклонили запрос {funcs.get_user_name_by_id(str(swap_request['message_from'].chat.id))}")


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
        f"Вы поменялись местом с {funcs.get_user_name_by_id(str(swap_request['message_from'].chat.id))}")
    await message.answer(f"Очередь {swap_request['queue_name']}",
                         reply_markup=get_inline_users_in_queue(funcs.get_queue(swap_request['queue_name']),
                                                                swap_request['queue_name'],
                                                                str(swap_request['message_to'].chat.id)))
    await bot.send_message(chat_id=swap_request['message_from'].chat.id,
                           text=f"Вы поменялись местом с {funcs.get_user_name_by_id(str(swap_request['message_to'].chat.id))}")
    await bot.send_message(chat_id=swap_request['message_from'].chat.id, text=f"Очередь {swap_request['queue_name']}",
                           reply_markup=get_inline_users_in_queue(funcs.get_queue(swap_request['queue_name']),
                                                                  swap_request['queue_name'],
                                                                  str(swap_request['message_to'].chat.id)))


async def show_help(message: types.Message, bot: Bot):
    await message.answer(text='В клавиатуре бота выберете \'Очереди\' для того чтобы выбрать очередь\n'
                              'Выберете кнопку с названием очереди которую хотите посмотреть\n'
                              'Выберете \'Добавиться\' или \'Добавиться в место\' если хотите встать в очередь\n'
                              'Если вы встали в очередь, вы нажатием на имя другого члена очереди можете отправить ему запрос на смену мест\n'
                              'Всё собственно... что ещё можно делать(если это будет вообще реализовано) вам знать пока не надо.')


async def debug_info(message: types.Message, bot: Bot):
    print(util_data.swap_requests.keys())
    print(util_data.last_bot_message_id)
    print(util_data.queue_name)
    print(util_data.last_action)


async def ping_all_users(bot: Bot, s):
    registered_users = funcs.get_registered_users()
    users = list(map(int, registered_users))
    for user_id in users:
        try:
            await bot.send_message(chat_id=user_id, text=s)
        except exceptions.TelegramBadRequest:
            logging.error(f"Target [ID:{user_id}]: BadRequest")
        except exceptions.TelegramNotFound:
            logging.error(f"Target [ID:{user_id}]: invalid user ID")
        except exceptions.TelegramRetryAfter as e:
            logging.error(
                f"Target [ID:{user_id}]: Flood limit is exceeded. "
                f"Sleep {e.retry_after} seconds."
            )
            await sleep(e.retry_after)
            return await bot.send_message(chat_id=user_id, text=s)
        except exceptions.TelegramAPIError:
            logging.exception(f"Target [ID:{user_id}]: failed")
        else:
            logging.info(f"Target [ID:{user_id}]: success")


async def send_message_to_all_users(message: types.Message, bot: Bot):
    if message.from_user.id in ADMIN_ID:
        await ping_all_users(bot, message.text[3:])
    else:
        await message.answer('Вы не админ')
