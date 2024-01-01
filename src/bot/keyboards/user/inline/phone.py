from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def create_phone_mp(name: str, is_more: bool = False) -> InlineKeyboardMarkup:
    if is_more:
        get_link = "Получить еще ссылки"
    else:
        get_link = "Получить ссылки"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_link, callback_data=f"phone_link|{name}"
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
