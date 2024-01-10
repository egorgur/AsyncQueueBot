from aiogram import types, Bot

from core.data_files.funcs import get_all_queue_names

from core.keyboards.reply import reply_keyboard

from core.keyboards.inline import get_inline_keyboard


async def get_inline(message: types.Message, bot: Bot):
    await message.answer('inline klava', reply_markup=get_inline_keyboard())


async def start_command(message: types.Message, bot: Bot):
    await message.answer(f'Привет {message.from_user.first_name} gpownmw', reply_markup=reply_keyboard)


async def view_all_queues(message: types.Message, bot: Bot):
    names = get_all_queue_names()
    await message.answer(f'все очереди {names}')


async def get_photo(message: types.Message, bot: Bot):
    await message.answer('картинка')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, 'downloads/photo.png')
