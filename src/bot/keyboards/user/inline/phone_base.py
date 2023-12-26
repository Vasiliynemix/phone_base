from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

list_phone_base_mp = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Список", callback_data="phone_base_list"),
            InlineKeyboardButton(text="Добавить", callback_data="phone_base_add"),
        ],
    ],
)
