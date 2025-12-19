from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def location_label_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🏠 Дім", callback_data="location:home"),
                InlineKeyboardButton(text="💼 Робота", callback_data="location:work"),
            ]
        ]
    )

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def send_location_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Надіслати геолокацію", request_location=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
