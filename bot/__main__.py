import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
import dotenv

dotenv.load_dotenv()

dispatcher = Dispatcher()

@dispatcher.message(F.text)
async def message_text_echo_handler(message: Message) -> None:
    await message.answer(message.text)

@dispatcher.message(F.photo)
async def message_photo_echo_handler(message: Message) -> None:
    await message.answer_photo(message.photo[-1].file_id)

async def main() -> None:
    bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())