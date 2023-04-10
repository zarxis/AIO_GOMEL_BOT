from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def KeyB() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/weather'),
           KeyboardButton('/to_filter'))
    return kb
