from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states.location import LocationState
from keyboards.location import location_label_keyboard, send_location_keyboard
from services.weather_api import get_weather_by_coords

router = Router()


@router.message(Command("location"))
async def location_command_handler(message: Message, state: FSMContext):

    # 1: Ask user to choose a label (Home / Work)
    await state.set_state(LocationState.choosing_label)

    await message.answer(
        "Оберіть, яке це місце 👇",
        reply_markup=location_label_keyboard()
    )


@router.callback_query(F.data.startswith("location:"))
async def location_label_handler(callback: CallbackQuery, state: FSMContext):

     # 2: Save label (home/work) and ask for geolocation
    label = callback.data.split(":")[1]

    # Save chosen label in FSM
    await state.update_data(label=label)
    await state.set_state(LocationState.waiting_location)

    await callback.message.answer(
        "Тепер надішліть геолокацію 📍",
        reply_markup=send_location_keyboard()
    )

    await callback.answer()


@router.message(LocationState.waiting_location, F.location)
async def location_message_handler(
    message: Message,
    state: FSMContext,
    db
):
     # 3: Save geolocation in DB and show weather
    # Get label from FSM
    data = await state.get_data()
    label = data["label"]

    # Save location in database
    await db.save_location(
        telegram_id=message.from_user.id,
        label=label,
        lat=message.location.latitude,
        lon=message.location.longitude,
    )

    # Confirm saved location + remove keyboard
    await message.answer(
        "Локацію збережено ✅",
        reply_markup=ReplyKeyboardRemove()
    )

    # 4: Get weather for this location
    weather_text = await get_weather_by_coords(
        message.location.latitude,
        message.location.longitude
    )
    await message.answer(f"Поточна погода для {label}:\n{weather_text}")

    # Clear FSM
    await state.clear()
