
from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from db.database import Database

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message, db: Database):
    # Save the user in the database
    await db.add_user(
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.last_name or ""
    )

    # Create a keyboard to guide the user
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Використати збережену локацію")],
            [KeyboardButton(text="🌆 Ввести назву міста")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    text = (
        f"Привіт, {message.from_user.first_name}! 👋\n"
        "Я бот прогнозу погоди 🌤\n\n"
        "Що я вмію:\n"
        "• Показувати погоду за назвою міста\n"
        "• Зберігати твої місця (Дім, Робота)\n\n"
          "📍 Щоб зберегти геолокацію — введи /location\n"
#         "🌆 Або просто введи назву міста"
        "Щоб отримати погоду:\n"
        "1️⃣ Натисніть '📍 Використати збережену локацію', щоб отримати погоду за збереженою локацією\n"
        "2️⃣ Натисніть '🌆 Ввести назву міста', щоб ввести назву міста і отримати прогноз"
    )

    await message.answer(text, reply_markup=kb)
