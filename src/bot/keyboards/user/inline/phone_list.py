from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def create_bookmarks_keyboard(
    name_list: list[str], page: int, has_more: bool
) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    last_name = None
    if len(name_list) % 2 != 0:
        last_name = name_list[-1]
        name_list = name_list[:-1]

    for i in range(0, len(name_list), 2):
        kb_builder.row(
            InlineKeyboardButton(
                text=f"{name_list[i]}",
                callback_data=f"phone_name|{name_list[i]}",
            ),
            InlineKeyboardButton(
                text=f"{name_list[i + 1]}",
                callback_data=f"phone_name|{name_list[i + 1]}",
            ),
        )

    if last_name is not None:
        kb_builder.row(
            InlineKeyboardButton(
                text=f"{last_name}",
                callback_data=f"phone_name|{last_name}",
            )
        )

    if has_more:
        if page == 0:
            kb_builder.row(
                InlineKeyboardButton(
                    text="➡️",
                    callback_data=f"next_page|{page + 1}",
                )
            )
        else:
            kb_builder.row(
                InlineKeyboardButton(
                    text="⬅️",
                    callback_data=f"prev_page|{page - 1}",
                ),
                InlineKeyboardButton(
                    text="➡️",
                    callback_data=f"next_page|{page + 1}",
                ),
            )
    else:
        if page != 0:
            kb_builder.row(
                InlineKeyboardButton(
                    text="⬅️",
                    callback_data=f"prev_page|{page - 1}",
                )
            )

    kb_builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data="phone_base_list_back",
        )
    )

    return kb_builder.as_markup()
