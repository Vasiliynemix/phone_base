from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

yes_no_mp = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да", callback_data="yes"),
            InlineKeyboardButton(text="❌ Нет", callback_data="no"),
        ],
    ],
)
