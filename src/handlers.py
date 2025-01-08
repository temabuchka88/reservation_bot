import os
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.input import MessageInput
from aiogram.fsm.state import StatesGroup, State
from src.config import settings
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from aiogram_dialog import (
    Dialog,
    DialogManager,
    setup_dialogs,
    StartMode,
    Window,
)
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from main import bot

router = Router()


class BookingSG(StatesGroup):
    waiting_for_booking = State()


async def send_to_admin(chat_id: int, message: str):
    await bot.send_message(chat_id, message, parse_mode="Markdown")


async def process_booking(message: Message, dialog_manager: DialogManager, bot: Bot):
    user_name = message.from_user.username or "гость"
    booking_details = message.text
    info_message = (
        f"🍽️ *Новое бронирование стола* 🍽️\n"
        f"Пользователь: @{user_name}\n"
        f"Детали: {booking_details}"
    )
    await send_to_admin(settings.ADMIN_GROUP, info_message)

    await message.answer(
        "Благодарим за информацию! В скором времени с вами свяжется наш сотрудник для подтверждения брони.\n\n"
        "Если вы хотите забронировать столик еще раз на другую дату — просто напишите желаемую дату, время и количество человек."
    )
    # await dialog_manager.reset_stack()


main_window = Window(
    Format(
        "Здравствуйте!\n"
        "Для бронирования столика, сообщите пожалуйста номер телефона для связи, "
        "желаемое время и дату посещения, а также количество гостей."
    ),
    MessageInput(process_booking),
    state=BookingSG.waiting_for_booking,
)

dialog = Dialog(main_window)


# @router.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    # dialog_manager.dialog_data["name"] = message.from_user.first_name or "гость"
    # print(user_name)
    await dialog_manager.start(
        BookingSG.waiting_for_booking,
        mode=StartMode.RESET_STACK,
        # data={"name": user_name},
    )
