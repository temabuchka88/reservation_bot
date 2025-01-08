import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from src import handlers
from src.config import settings
from aiogram_dialog import setup_dialogs
from aiogram.filters import CommandStart

bot_token = settings.BOT_TOKEN


bot = Bot(bot_token)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.register(handlers.start, CommandStart())
    dp.include_router(handlers.dialog)
    setup_dialogs(dp)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
