from aiogram.fsm.state import State, StatesGroup


class Booking(StatesGroup):
    start_date = State()  # Ожидание даты заезда
    end_date = State()  # Ожидание даты выезда
    choosing_room = State()  # Ожидание выбора домика (из фейкового списка)
    confirm = State()  # Подтверждение брони
