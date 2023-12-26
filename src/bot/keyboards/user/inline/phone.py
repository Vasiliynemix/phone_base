from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def create_phone_mp(name: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Получить ссылки", callback_data=f"phone_link|{name}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Получить файл", callback_data=f"phone_get|{name}"
                ),
                InlineKeyboardButton(
                    text="Изменить файл", callback_data=f"phone_edit_file|{name}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Изменить текст", callback_data=f"phone_edit_text|{name}"
                ),
            ],
            [InlineKeyboardButton(text=f"Отмена", callback_data=f"phone_cancel")],
        ],
    )
