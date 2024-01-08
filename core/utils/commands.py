from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='testcommand'
        ),
        BotCommand(
            command='help',
            description='all commands list'
        ),
        BotCommand(
            command='cancel',
            description='Отмена ввода'
        )
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
