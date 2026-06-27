from aiogram.types import InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

rooms = ["House №1", "House №2"]


async def rooms_kb() -> InlineKeyboardMarkup:
    """Заглушка выбора свободных номеров"""
    builder = InlineKeyboardBuilder()

    for room in rooms:
        builder.add(
            InlineKeyboardButton(
                text=room,
                callback_data=f"room_{room.lower().replace(' ', '_')}"
            )
        )

    # Если хочешь, чтобы домики шли в колонну
    builder.adjust(1)

    return builder.as_markup()
