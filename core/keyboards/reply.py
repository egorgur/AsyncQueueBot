from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Очереди'
        ),
        KeyboardButton(
            text='...'
        ),
    ],
    [
        KeyboardButton(
            text=',,,'
        ),
        KeyboardButton(
            text='mmmm'
        ),
    ]
], resize_keyboard=True, input_field_placeholder='Выберите кнопку')
