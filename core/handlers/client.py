from json import dumps

from aiogram import types, Bot
from aiogram.filters.command import Command

from core.keyboards.reply import get_start_game_keyboard

from config import PATH_TO_DATABASE
from database.db_work import get_info_from_db
from database.querysets import GET_ACTIVE_SESSION


async def cmd_start(message: types.Message):
    await get_start_game_keyboard(message)


async def cmd_quiz(message: types.Message):
    await message.answer(f"Давайте начнем квиз!")
    user_id = message.from_user.id
    active_session = await get_info_from_db(GET_ACTIVE_SESSION, user_id)
    if len(active_session) == 0:
        # Запустить новый квиз
        # await new_quiz(message)
        pass
    else:
        await message.answer(f"У вас сохранилась не заверщенная сессия, желаете продолжить?")

    # await new_quiz(message)
















# Удалить, сервисная команда
async def cmd_get_info_message(message: types.Message, bot: Bot):
    await message.answer(dumps(message.model_dump(), default=str))
