from aiogram.fsm.state import StatesGroup, State

class CityState(StatesGroup):
    waiting_for_city = State()  # User should enter city name
