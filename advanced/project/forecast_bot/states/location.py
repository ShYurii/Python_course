from aiogram.fsm.state import StatesGroup, State


class LocationState(StatesGroup):
    choosing_label = State()   # user chooses Home / Work
    waiting_location = State()  # user sends geo
