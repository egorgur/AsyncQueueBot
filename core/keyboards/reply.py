from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Очереди'
        ),
        KeyboardButton(
            text='Очереди'
        ),
    ],
    [
        KeyboardButton(
            text='Дедлайны'
        ),
        KeyboardButton(
            text='О боте'
        ),
    ]
], resize_keyboard=True, input_field_placeholder='Выберите кнопку')
