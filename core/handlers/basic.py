from aiogram import types, Bot

from core.data_files import funcs

from core.keyboards.reply import reply_keyboard

from core.keyboards.inline import get_inline_queues_control, get_inline_queues_keyboard


async def start_command(message: types.Message, bot: Bot):
    await message.answer(f'Привет {message.from_user.first_name} gpownmw', reply_markup=reply_keyboard)


async def view_all_queues(message: types.Message, bot: Bot):
    names = funcs.get_all_queue_names()
    await message.answer(f'все очереди {names}', reply_markup=get_inline_queues_keyboard(names))


async def view_queues_control_menu(message: types.Message, bot: Bot):
    names = funcs.get_all_queue_names()
    await message.answer(f'все очереди {names}', reply_markup=get_inline_queues_control(names))


async def get_photo(message: types.Message, bot: Bot):
    await message.answer('картинка')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, 'downloads/photo.png')
