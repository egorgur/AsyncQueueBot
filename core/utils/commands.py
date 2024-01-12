from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Бот запоминает ваше имя и оно будет отображатся в очередях'
        ),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
