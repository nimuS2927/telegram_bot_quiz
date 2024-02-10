from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types


async def get_start_game_keyboard(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text='Начать игру'))
    await message.answer('Добро пожаловать в квиз!',
                         reply_markup=builder.as_markup(
                             resize_keyboard=True,
                             one_time_keyboard=True)
                         )

# async def get_start_game_keyboard(message: types.Message):
#     builder = InlineKeyboardBuilder()
#     builder.add(InlineKeyboardButton(text='Начать игру', callback_data='Добро'))
#     await message.answer('Добро пожаловать в квиз!', reply_markup=builder.as_markup(resize_keyboard=True))
