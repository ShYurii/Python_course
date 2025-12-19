from aiogram import Router, F
from aiogram.types import Message
from db.database import Database
from services.weather_api import get_weather_by_coords

router = Router()

@router.message(F.text == "📍 Використати збережену локацію")
async def weather_by_saved_location(message: Message, db: Database):
    # Try to get saved home location
    location = await db.get_location_by_label(
        telegram_id=message.from_user.id,
        label="home"
    )

    if not location:
        await message.answer(
            "У вас ще немає збереженої локації 😕\n"
            "Введіть /location щоб додати."
        )
        return

    await message.answer("Отримую погоду для збереженої локації ⏳")

    weather_text = await get_weather_by_coords(
        location["lat"],
        location["lon"]
    )

    await message.answer(weather_text)

