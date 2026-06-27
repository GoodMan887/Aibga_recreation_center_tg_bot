import html
import logging
from datetime import (
    date,
    datetime,
)

from aiogram import Bot, F, Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app import config
from app.keyboards.inline.available_rooms import rooms_kb
from app.keyboards.inline.calendar import get_custom_calendar
from app.messages.booking import (
    choose_start_date_msg,
    start_date_selected_msg,
    available_rooms_by_date,
    end_of_booking_msg,
    start_msg,
)
from app.states import Booking

logger = logging.getLogger(__name__)

router = Router()


# 1. Начало записи из главного меню
@router.message(F.text == config.BUTTON_BOOKING)
async def start_booking_from_menu(message: types.Message, state: FSMContext):
    current_date = date.today()
    await state.set_state(Booking.start_date)
    await message.answer(text=choose_start_date_msg,
                         reply_markup=await get_custom_calendar(
                             current_date.year, current_date.month
                             )
                         )


# 2. Дата заезда выбрана, прошу ввести дату выезда
@router.callback_query(StateFilter(Booking.start_date), F.data.startswith("cal_set_"))
async def process_start_date(callback: types.CallbackQuery, state: FSMContext):
    # Извлекаем дату из callback_data (например, cal_set_2026-02-20)
    start_date_str = callback.data.replace("cal_set_", "")
    selected_start_date_obj = datetime.fromisoformat(start_date_str).date()

    current_date = date.today()
    formatted_date = selected_start_date_obj.strftime("%d.%m.%Y")

    await state.update_data(start_date=start_date_str)
    await state.set_state(Booking.end_date)

    # Редактируем календарь и сообщение на выбор даты выезда
    await callback.message.edit_text(
        text=start_date_selected_msg.format(formatted_date=formatted_date),
        reply_markup=await get_custom_calendar(
                            selected_start_date_obj.year,
                            selected_start_date_obj.month,
                            selected_start_date_obj
                             ),
    )

    await callback.answer()


# 2.2. Хэндлеры для навигации по календарю (вперед/назад)
@router.callback_query(F.data.startswith("cal_prev_") | F.data.startswith("cal_next_"))
async def process_calendar_navigation(callback: types.CallbackQuery, state: FSMContext):
    # Разбираем callback_data (например, cal_next_2026_6)
    parts = callback.data.split("_")
    action = parts[1]  # prev или next
    year = int(parts[2])
    month = int(parts[3])

    # Вычисляем новый месяц и год
    if action == "next":
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
    elif action == "prev":
        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1

    # Проверяем, на каком шаге FSM находится пользователь,
    # чтобы правильно подтянуть start_date (если она уже выбрана)
    current_state = await state.get_state()
    start_date_obj = None
    text_msg = choose_start_date_msg

    if current_state == Booking.end_date:
        user_data = await state.get_data()
        start_date_str = user_data.get("start_date")
        if start_date_str:
            start_date_obj = datetime.fromisoformat(start_date_str).date()
            formatted_date = start_date_obj.strftime("%d.%m.%Y")
            text_msg = start_date_selected_msg.format(formatted_date=formatted_date)

    # Обновляем календарь в текущем сообщении
    await callback.message.edit_text(
        text=text_msg,
        reply_markup=await get_custom_calendar(year, month, start_date_obj)
    )
    await callback.answer()

# 3. Дата выезда выбрана, возвращаю доступные варианты
@router.callback_query(StateFilter(Booking.end_date), F.data.startswith("cal_set_"))
async def process_end_date(callback: types.CallbackQuery, state: FSMContext):
    # Извлекаем дату из callback_data (например, cal_set_2026-02-20)
    end_date_str = callback.data.replace("cal_set_", "")
    selected_end_date_obj = datetime.fromisoformat(end_date_str).date()

    user_data = await state.get_data()
    start_date_obj = datetime.fromisoformat(user_data["start_date"]).date()
    formatted_start_date = start_date_obj.strftime("%d.%m.%Y")
    formatted_end_date = selected_end_date_obj.strftime("%d.%m.%Y")

    await state.update_data(end_date=end_date_str)
    await state.set_state(Booking.choosing_room)

    # Удаляю календарь и вывожу доступные варианты
    await callback.message.delete()
    await callback.message.answer(text=available_rooms_by_date.format(formatted_start_date=formatted_start_date,
                                                                      formatted_end_date=formatted_end_date),
                          reply_markup= await rooms_kb()
                          )

    await callback.answer()


# 4. Домик выбран, завершаю бронь
@router.callback_query(StateFilter(Booking.choosing_room), F.data.startswith("room_"))
async def confirm_booking(callback: types.CallbackQuery, state: FSMContext):
    room_data = callback.data.replace('room_', '')

    # Небольшая оптимизация разбора названия
    room = "House №1" if room_data == "house_№1" else "House №2"

    # ИСПРАВИЛ: .edit_text() сработает, так как на шаге 3 мы прислали новое сообщение с инлайн кнопками
    await callback.message.edit_text(text=end_of_booking_msg.format(room=room))
    await callback.answer()
    await state.clear()
