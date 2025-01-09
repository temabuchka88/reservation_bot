from aiogram import Router
from aiogram.types import Message
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.input import MessageInput
from aiogram.fsm.state import StatesGroup, State
from src.config import settings
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message

from aiogram_dialog import (
    Dialog,
    DialogManager,
    StartMode,
    Window,
)
from aiogram_dialog.widgets.text import Const
from main import bot

router = Router()


class BookingSG(StatesGroup):
    first_booking = State()
    waiting_for_booking = State()


async def send_to_admin(chat_id: int, message: str):
    await bot.send_message(chat_id, message, parse_mode="Markdown")


async def first_booking(
    message: Message, message_input: MessageInput, dialog_manager: DialogManager
):
    user_name = message.from_user.username or "гость"
    booking_details = message.text
    info_message = (
        f"🍽️ *Новое бронирование стола* 🍽️\n"
        f"Пользователь: @{user_name}\n"
        f"Детали: {booking_details}"
    )
    await send_to_admin(settings.ADMIN_GROUP, info_message)

    await dialog_manager.switch_to(BookingSG.waiting_for_booking)


async def process_booking(
    message: Message, message_input: MessageInput, dialog_manager: DialogManager
):

    user_name = message.from_user.username or "гость"
    booking_details = message.text
    info_message = (
        f"🍽️ *Новое бронирование стола* 🍽️\n"
        f"Пользователь: @{user_name}\n"
        f"Детали: {booking_details}"
    )
    await send_to_admin(settings.ADMIN_GROUP, info_message)

    await dialog_manager.switch_to(BookingSG.waiting_for_booking)


dialog = Dialog(
    Window(
        Format(
            "Здравствуйте,{event.from_user.first_name}!\n"
            "Для бронирования столика, сообщите пожалуйста номер телефона для связи, "
            "желаемое время и дату посещения, а также количество гостей."
        ),
        MessageInput(first_booking),
        state=BookingSG.first_booking,
    ),
    Window(
        Const(
            "Благодарим за информацию! В скором времени с вами свяжется наш сотрудник для подтверждения брони.\n\n"
            "Если вы хотите забронировать столик еще раз на другую дату — просто напишите желаемую дату, время и количество человек."
        ),
        MessageInput(process_booking),
        state=BookingSG.waiting_for_booking,
    ),
)


async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        BookingSG.first_booking,
        mode=StartMode.RESET_STACK,
    )
