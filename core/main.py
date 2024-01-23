from aiogram import Bot, Dispatcher

import asyncio
import logging

from handlers.basic import start_command, get_photo, view_queues_control_menu, view_all_queues, reply_processing, \
    accepting_swap_request, deni_swap_request, debug_info, show_help, send_message_to_all_users, cancel_swap_request
from handlers.callback import select_queue, delete_user, add_user, show_queues, delete_queue, rename_queue_call, \
    make_queue_call, spec_user_add_menu, spec_user_add, user_swap_request_registrator

from settings import TOKEN, ADMIN_ID
from aiogram.filters import Command
from aiogram import F

from utils.commands import set_commands
from utils.callbackdata import QueuesButtonInfo, UserDeletion, UserAddition, ReturnToQueues, DeleteQueue, \
    RenameQueue, MakeQueue, SpecUserAdditionCall, SpecUserAddition, UserToSwap, NoneInfo

Token = TOKEN


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(ADMIN_ID[0], 'бот запущен')


async def stop_bot(bot: Bot):
    await bot.send_message(ADMIN_ID[0], 'бот опущен')


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

    dp.message.register(deni_swap_request, Command(commands=['deni']))
    dp.message.register(accepting_swap_request, Command(commands=['swap']))
    dp.message.register(cancel_swap_request, Command(commands=['cancel']))
    dp.message.register(debug_info, Command(commands=['debug']))
    dp.message.register(reply_processing, F.reply_to_message)
    dp.message.register(send_message_to_all_users, F.text.startswith('msg'))
    dp.message.register(show_help, F.text == 'Помощь')
    dp.message.register(view_all_queues, F.text == 'Очереди')
    dp.message.register(view_queues_control_menu, F.text == 'Управление очередями')
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
