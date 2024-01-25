from datetime import datetime

from data_files import funcs

from asyncio import sleep
from aiogram import types, Bot

from handlers.basic import ping_all_users


async def timed_queues_processor(Token):
    bot = Bot(Token, parse_mode='HTML')
    while True:
        queues = funcs.get_all_timed_queue_data()
        for i in range(len(queues)):
            print(queues[i][1]['time'], queues[i][1]['date'])
            if (str(datetime.now().strftime("%H.%M")) == queues[i][1]['time']) and (
                    str(datetime.now().date().day) == queues[i][1]['date']):
                funcs.make_new_queue(queues[i][0])
                await ping_all_users(bot, f"Создана очередь {queues[i][0]} {queues[i][1]['time']}")
                funcs.delete_timed_queue(queues[i][0])
        await sleep(10)
