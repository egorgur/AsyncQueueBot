from aiogram import Bot
from aiogram.types import CallbackQuery
from core.utils.callbackdata import QueuesButtonInfo


async def select_test(call: CallbackQuery, bot: Bot, callback_data: QueuesButtonInfo):
    button = callback_data.button_name
    answer = f'inline кнопка {button}'
    await call.message.answer(answer)
    await call.answer()
