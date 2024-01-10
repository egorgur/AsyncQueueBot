from aiogram import types, Bot

from core.data_files import funcs

from core.keyboards.reply import reply_keyboard

from core.keyboards.inline import get_inline_queues_control, get_inline_queues_keyboard

from core.utils.utils import util_data


async def start_command(message: types.Message, bot: Bot):
    await message.answer(f'Привет {message.from_user.first_name} gpownmw', reply_markup=reply_keyboard)


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


async def rename_process(message: types.Message, bot: Bot):
    if message.reply_to_message.message_id == util_data.last_bot_message_id + 1:
        funcs.rename_queue(util_data.queue_name, message.text)
        await message.answer('Очередь переименована')


async def make_process(message: types.Message, bot: Bot):
    if message.reply_to_message.message_id == util_data.last_bot_message_id + 1:
        funcs.make_new_queue(message.text)
        funcs.add_user_to_last_position_in_queue(str(message.from_user.id), message.text)
        await message.answer('Очередь создана')
