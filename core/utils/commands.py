from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы, идентично команде "run" или "старт"'
        ),
        BotCommand(
            command='info',
            description='Получить информацию о сообщении, сервисная команда (УДАЛИТЬ)'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())

