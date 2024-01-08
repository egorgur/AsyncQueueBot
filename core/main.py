from aiogram import Bot, Dispatcher

import asyncio
import logging

from core.handlers.basic import start_command, get_photo, get_inline
from core.handlers.callback import select_test

from core.settings import settings

from aiogram.filters import Command
from aiogram import F

from core.utils.commands import set_commands
from core.utils.callbackdata import ButtonInfo

Token = settings.bots.bot_token
admin_id = settings.bots.admin_id


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(admin_id, 'бот запущен')


async def stop_bot(bot: Bot):
    await bot.send_message(admin_id, 'бот опущен')


def register(dp_obj: Dispatcher):
    dp_obj.startup.register(start_bot)
    dp_obj.shutdown.register(stop_bot)
    dp_obj.message.register(get_photo, F.photo)
    dp_obj.message.register(start_command, Command(commands=['start']))
    dp_obj.message.register(get_inline, Command(commands=['inline']))
    dp_obj.callback_query.register(select_test, ButtonInfo.filter())
    return dp_obj


dp = Dispatcher()
dp = register(dp)


async def start():
    bot = Bot(Token, parse_mode='HTML')
    logging.basicConfig(level=logging.NOTSET,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
