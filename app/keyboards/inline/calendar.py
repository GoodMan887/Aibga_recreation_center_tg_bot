import calendar
from datetime import date

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.constants.custom_calendar import (
    days,
    months,
)
from app.messages.booking import cancel_booking_kb_msg


async def get_custom_calendar(year: int, month: int, start_date: date = None):
    builder = InlineKeyboardBuilder()
    today = date.today()

    # Месяц и год
    month_names = months
    builder.row(
        InlineKeyboardButton(text=f"{month_names[month - 1]} {year}", callback_data="ignore")
    )

    # Дни недели
    week_days = days
    builder.row(*[InlineKeyboardButton(text=d, callback_data="ignore") for d in week_days])

    month_calendar = calendar.monthcalendar(year, month)

    for week in month_calendar:
        buttons = []
        for day in week:
            if day == 0:
                buttons.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
                continue

            current_date = date(year, month, day)

            # 1. Защита от прошлых дат
            if current_date < today:
                buttons.append(InlineKeyboardButton(text="❌", callback_data="ignore"))

            # 2. Если дата заезда уже выбрана, блокируем её саму и всё, что до неё
            elif start_date and current_date <= start_date:
                # Визуально выделяем день заезда
                if current_date == start_date:
                    buttons.append(InlineKeyboardButton(text="🛫", callback_data="ignore"))
                else:
                    buttons.append(InlineKeyboardButton(text="❌", callback_data="ignore"))

            # 3. Доступная для выбора дата
            else:
                buttons.append(
                    InlineKeyboardButton(
                        text=str(day), callback_data=f"cal_set_{current_date.isoformat()}"
                    )
                )
        builder.row(*buttons)

    # Навигация
    nav_buttons = []

    # Логика для кнопки НАЗАД (<<)
    # Если дата заезда уже выбрана (start_date передана)
    if start_date:
        # Скрываем кнопку, если текущий отображаемый месяц равен или МЕНЬШЕ месяца заезда
        # (Пользователь не сможет уйти в прошлое относительно своего заезда)
        if not (year <= start_date.year and month <= start_date.month):
            nav_buttons.append(
                InlineKeyboardButton(text="<<", callback_data=f"cal_prev_{year}_{month}")
            )
    else:
        # Если дата заезда еще НЕ выбрана, скрываем кнопку только для текущего реального месяца
        if not (year == today.year and month == today.month):
            nav_buttons.append(
                InlineKeyboardButton(text="<<", callback_data=f"cal_prev_{year}_{month}")
            )

    nav_buttons.append(
        InlineKeyboardButton(text=">>", callback_data=f"cal_next_{year}_{month}")
    )

    builder.row(*nav_buttons)
    builder.row(InlineKeyboardButton(text=cancel_booking_kb_msg, callback_data="cancel_booking"))
    return builder.as_markup()
