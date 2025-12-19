from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from db.database import Database
from states.city import CityState
from services.weather_api import get_weather_by_city

router = Router()

@router.message(F.text == "🌆 Ввести назву міста")
async def enter_city_handler(message: Message, state: FSMContext):
    #  Ask user to enter city
    await state.set_state(CityState.waiting_for_city)
    await message.answer(
        "Введіть назву міста, щоб отримати погоду:",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(CityState.waiting_for_city)
async def city_weather_handler(message: Message, state: FSMContext):
    city_name = message.text.strip()

    #  Request weather from OpenWeather
    weather_text = await get_weather_by_city(city_name)

    #  Send result to user
    await message.answer(weather_text)

    # Clear state
    await state.clear()
