import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram import F

from config import TOKEN

from core.handlers.client import cmd_start, cmd_get_info_message, cmd_quiz, cmd_game, cmd_save_answer, cmd_end_game, \
    choice_session
from core.utils.commands import set_commands
from core.utils.statesquiz import StepsQuiz

from database.db_create import main_db_create


async def on_start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(chat_id=1817810653, text=f'Bot started')


async def on_stop_bot(bot: Bot):
    await bot.send_message(chat_id=1817810653, text=f'Bot stopped')


async def main():

    # Создание БД
    await main_db_create()

    # Создание экземпляров бота и диспетчера
    bot = Bot(token=TOKEN, parse_mode='HTML')
    dp = Dispatcher()

    # Настройка базового логирования
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(name)s -'
                               ' %(message)s')

    # Регистрация действий на начало и окончание работы бота
    dp.startup.register(on_start_bot)
    dp.shutdown.register(on_stop_bot)

    # Регистрация команд для бота
    dp.message.register(cmd_start, Command(commands=['start', 'run', 'старт']))
    dp.message.register(cmd_quiz, F.text == 'Начать игру')
    dp.message.register(cmd_game, StepsQuiz.GET_QUESTION)
    dp.message.register(cmd_save_answer, StepsQuiz.SAVE_ANSWER)
    dp.message.register(cmd_end_game, StepsQuiz.END_GAME)
    dp.message.register(choice_session, StepsQuiz.CHOICE_SESSION)

    # Сервесные команды на период разработки
    dp.message.register(cmd_get_info_message, F.text == 'info')
    dp.message.register(cmd_get_info_message, Command(commands=['info']))

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
