from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.keyboards.reply.main_menu import main_menu_kb
from app.messages.booking import start_msg

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    Обработка команды /start
    """
    await message.answer(start_msg, parse_mode="HTML", reply_markup=main_menu_kb())
