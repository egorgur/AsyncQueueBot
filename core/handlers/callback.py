from aiogram import Bot
from aiogram.types import CallbackQuery
from core.utils.callbackdata import ButtonInfo

# async def select_test(call: CallbackQuery, bot: Bot):
#     button = call.data.split('_')[0]
#     button_data = call.data.split('_')[1]
#     answer = f'inline кнопка {button}, её данные {button_data}'
#     await call.message.answer(answer)
#     await call.answer()

async def select_test(call: CallbackQuery, bot: Bot, callback_data: ButtonInfo):
    button = callback_data.button_name
    button_data = callback_data.button_data
    answer = f'inline кнопка {button}, её данные {button_data}'
    await call.message.answer(answer)
    await call.answer()
