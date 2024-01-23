from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Очереди'
        ),
        KeyboardButton(
            text='Управление очередями'
        ),
    ],
    [
        KeyboardButton(
            text='Помощь'
        )
    ]
], resize_keyboard=True, input_field_placeholder='Выберите кнопку')
