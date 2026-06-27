from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.config import BUTTON_INFO, BUTTON_BOOKING, BUTTON_CONTACTS


def main_menu_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    # Добавляем кнопки (каждая кнопка — это просто объект KeyboardButton с текстом)
    builder.add(KeyboardButton(text=BUTTON_INFO))
    builder.add(KeyboardButton(text=BUTTON_BOOKING))
    builder.add(KeyboardButton(text=BUTTON_CONTACTS))

    # Выстраиваем кнопки по одной в ряд
    builder.adjust(1)

    # resize_keyboard=True делает кнопки компактными (не на пол-экрана)
    return builder.as_markup(resize_keyboard=True)
