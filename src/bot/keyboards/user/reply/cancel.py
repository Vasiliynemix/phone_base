from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

cancel_mp = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отмена")],
    ],
    resize_keyboard=True,
)