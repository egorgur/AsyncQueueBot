from aiogram import Bot, Dispatcher

import asyncio
import logging

from core.handlers.basic import start_command, get_photo, view_queues_control_menu, view_all_queues, reply_processing, \
    accepting_swap_request
from core.handlers.callback import select_queue, delete_user, add_user, show_queues, delete_queue, rename_queue_call, \
    make_queue_call, spec_user_add_menu, spec_user_add, user_swap_request_registrator

from core.settings import settings
from aiogram.filters import Command
from aiogram import F

from core.utils.commands import set_commands
from core.utils.callbackdata import QueuesButtonInfo, UserDeletion, UserAddition, ReturnToQueues, DeleteQueue, \
    RenameQueue, MakeQueue, SpecUserAdditionCall, SpecUserAddition, UserToSwap, NoneInfo

Token = settings.bots.bot_token
admin_id = settings.bots.admin_id


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(admin_id, 'бот запущен')


async def stop_bot(bot: Bot):
    await bot.send_message(admin_id, 'бот опущен')


dp = Dispatcher()


async def start():
    bot = Bot(Token, parse_mode='HTML')
    logging.basicConfig(level=logging.NOTSET,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(get_photo, F.photo)
    dp.message.register(start_command, Command(commands=['start']))

    dp.callback_query.register(select_queue, QueuesButtonInfo.filter())
    dp.callback_query.register(delete_user, UserDeletion.filter())
    dp.callback_query.register(add_user, UserAddition.filter())
    dp.callback_query.register(show_queues, ReturnToQueues.filter())
    dp.callback_query.register(delete_queue, DeleteQueue.filter())
    dp.callback_query.register(rename_queue_call, RenameQueue.filter())
    dp.callback_query.register(make_queue_call, MakeQueue.filter())
    dp.callback_query.register(spec_user_add_menu, SpecUserAdditionCall.filter())
    dp.callback_query.register(spec_user_add, SpecUserAddition.filter())
    dp.callback_query.register(user_swap_request_registrator, UserToSwap.filter())

    dp.message.register(accepting_swap_request, Command(commands=['swap']))
    dp.message.register(reply_processing, F.reply_to_message)
    dp.message.register(view_all_queues, F.text == 'Очереди')
    dp.message.register(view_queues_control_menu, F.text == 'Управление очередями')
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
