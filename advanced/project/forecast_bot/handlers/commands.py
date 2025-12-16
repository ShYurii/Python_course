
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Привіт! 👋\n"
        "Я бот прогнозу погоди 🌤\n\n"
        "Надішли свою геолокацію 📍 або введи назву міста."
    )
