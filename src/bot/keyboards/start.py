from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

start_mp = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱Базы номеров")],
    ],
    resize_keyboard=True,
)
