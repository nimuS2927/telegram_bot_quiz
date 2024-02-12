from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types


def get_start_game_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text='Начать игру'))
    return builder.as_markup(resize_keyboard=True,
                             one_time_keyboard=True)


def get_confirm_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text='Yes'),
        KeyboardButton(text='No')
                )
    return builder.as_markup(resize_keyboard=True,
                             one_time_keyboard=True)


def get_choice_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text='1'),
        KeyboardButton(text='2'),
        KeyboardButton(text='3'),
        KeyboardButton(text='4'),
                )
    return builder.as_markup(resize_keyboard=True,
                             one_time_keyboard=True)
