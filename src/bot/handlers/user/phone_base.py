import shutil

import pyperclip
from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery
from loguru import logger

from src.bot.handlers.funks import (
    get_list_random_text,
    get_file_text,
    check_file_text,
    create_file_text,
    create_text_links,
    split_text,
    copy_text_to_clipboard, get_list_param_text,
)
from src.bot.keyboards.start import start_mp
from src.bot.keyboards.user.inline.phone import create_phone_mp
from src.bot.keyboards.user.inline.phone_base import list_phone_base_mp
from src.bot.keyboards.user.inline.phone_list import (
    create_regex_pagination_mp,
)
from src.bot.keyboards.user.reply.cancel import cancel_mp
from src.bot.keyboards.yes_no import yes_no_mp
from src.bot.lexicon.lexicon import (
    CANCEL_MSG,
    BASES_MSG,
    ADD_CSV_MSG,
    BACK_MSG,
    ADD_NO_CSV_MSG,
    ADD_WRONG_FORMAT_CSV_MSG,
    EDIT_FILE_SUCCESS_MSG,
    phone_name_add_text_msg,
    ADD_PHONE_NAME_EXISTS_MSG,
    phone_name_long_msg,
    ADD_PHONE_TEXT_MSG,
    phone_text_not_valid_msg,
    EDIT_TEXT_SUCCESS_MSG,
    phone_add_new_msg,
    ADD_PHONE_SUCCESS_MSG,
    ADD_PHONE_CANCEL_MSG,
    BASES_EMPTY_MSG,
    BASES_LIST_MSG,
    phone_base_click_msg,
    GET_LINKS_MSG,
    GET_LINKS_WRONG_MSG,
    ALL_NUMBERS_SHOWED_MSG,
    COPY_TEXT_ERROR_MSG,
    COPY_TEXT_SUCCESS_MSG,
    all_links_success_send_msg,
)
from src.bot.structures.state.user import (
    AddPhoneBaseState,
    EditPhoneBaseState,
    GetLinksState,
)
from src.config.config import cfg
from src.db.db import Database

router = Router()


@router.message(F.text == "Отмена")
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(CANCEL_MSG, reply_markup=start_mp)


@router.message(F.text == "📱Базы номеров")
async def phone_base(message: Message):
    await message.answer(BASES_MSG, reply_markup=list_phone_base_mp)


@router.callback_query(F.data == "phone_base_list_back")
@router.callback_query(F.data == "phone_cancel")
async def phone_base_list_back(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(BACK_MSG, reply_markup=list_phone_base_mp)


@router.callback_query(F.data == "phone_base_add")
async def phone_base_add(callback: Message, state: FSMContext):
    await callback.answer()
    await state.set_state(AddPhoneBaseState.csv)
    await callback.message.answer(ADD_CSV_MSG, reply_markup=cancel_mp)


@router.message(F.document, AddPhoneBaseState.csv)
@router.message(F.document, EditPhoneBaseState.file)
async def phone_base_csv(message: Message, state: FSMContext, db: Database, bot: Bot):
    if message.document.mime_type != "text/csv":
        await message.answer(ADD_NO_CSV_MSG, reply_markup=cancel_mp)
        return

    file_id = message.document.file_id

    file_text = await get_file_text(bot, file_id)
    # ok = check_file_text(file_text)
    # if not ok:
    #     await message.answer(
    #         ADD_WRONG_FORMAT_CSV_MSG,
    #         reply_markup=cancel_mp,
    #     )
    #     return

    current_state = await state.get_state()
    if current_state == EditPhoneBaseState.file:
        data = await state.get_data()
        name = data.get("name")
        await db.phone.update_numbers(
            user_id=message.from_user.id, name=name, numbers=file_text
        )

        await state.clear()
        await message.answer(EDIT_FILE_SUCCESS_MSG, reply_markup=start_mp)
        return

    await state.update_data(file_id=file_id)
    await state.set_state(AddPhoneBaseState.name)

    phones = await db.phone.get_all(user_id=message.from_user.id)

    phones_text = ""
    if len(phones) > 0:
        phones_text += "\nСписок загруженных имен:\n"
        phones_text += "\n".join([phone.name for phone in phones])

    await message.answer(
        phone_name_add_text_msg(phones_text),
        reply_markup=cancel_mp,
    )


@router.message(AddPhoneBaseState.csv)
async def phone_base_csv_not_document(message: Message):
    await message.answer(ADD_CSV_MSG, reply_markup=cancel_mp)


@router.message(F.text, AddPhoneBaseState.name)
async def phone_base_name(message: Message, state: FSMContext, db: Database):
    phone = await db.phone.get(user_id=message.from_user.id, name=message.text)
    if phone is not None:
        await message.answer(ADD_PHONE_NAME_EXISTS_MSG, reply_markup=cancel_mp)
        return

    if len(message.text) > 20:
        await message.answer(
            phone_name_long_msg(message.text),
            reply_markup=cancel_mp,
        )
        return

    await state.update_data(name=message.text)
    await state.set_state(AddPhoneBaseState.text)
    await message.answer(
        ADD_PHONE_TEXT_MSG,
        reply_markup=cancel_mp,
    )


@router.message(F.text, AddPhoneBaseState.text)
@router.message(F.text, EditPhoneBaseState.text)
async def phone_base_text(message: Message, state: FSMContext, db: Database):
    matches = get_list_random_text(message.text)
    params = get_list_param_text(message.text)

    check_open = len(matches) + len(params) == message.text.count("{")
    check_cancel = len(matches) + len(params) == message.text.count("}")
    check_pipe = len(matches) <= message.text.count("|")

    if not check_open or not check_cancel or not check_pipe:
        text_template = "\n".join(matches)
        await message.answer(
            phone_text_not_valid_msg(text_template),
            reply_markup=cancel_mp,
        )
        return

    current_state = await state.get_state()
    if current_state == EditPhoneBaseState.text:
        data = await state.get_data()
        name = data.get("name")
        await db.phone.update_text(
            user_id=message.from_user.id, name=name, text=message.text
        )
        await state.clear()
        await message.answer(EDIT_TEXT_SUCCESS_MSG, reply_markup=start_mp)
        return

    await state.update_data(text=message.text)
    data = await state.get_data()
    name = data.get("name")
    text = data.get("text")

    await state.set_state(AddPhoneBaseState.end)

    await message.answer(
        phone_add_new_msg(name, text),
        reply_markup=yes_no_mp,
        parse_mode="HTML",
    )


@router.callback_query(F.data == "yes", AddPhoneBaseState.end)
async def phone_base_yes(
    callback: CallbackQuery, state: FSMContext, bot: Bot, db: Database
):
    data = await state.get_data()
    name = data.get("name")
    text = data.get("text")
    file_id = data.get("file_id")

    file_text = await get_file_text(bot, file_id)

    await db.phone.new(
        user_id=callback.from_user.id,
        name=name,
        numbers=file_text,
        text=text,
    )

    await state.clear()
    await callback.answer()
    await callback.message.answer(ADD_PHONE_SUCCESS_MSG, reply_markup=start_mp)


@router.callback_query(F.data == "no", AddPhoneBaseState.end)
async def phone_base_yes(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.answer(ADD_PHONE_CANCEL_MSG, reply_markup=start_mp)


@router.callback_query(F.data == "phone_base_list")
async def phone_base_list(callback: CallbackQuery, state: FSMContext, db: Database):
    await callback.answer()
    page = 0
    await state.update_data(page=page)

    phones, has_more = await db.phone.get_pagination(
        user_id=callback.from_user.id, offset=page, limit=cfg.db.limit_phones
    )
    if len(phones) == 0:
        await callback.message.answer(BASES_EMPTY_MSG, reply_markup=start_mp)
        return

    name_list = [phone.name for phone in phones]

    await callback.message.edit_text(
        BASES_LIST_MSG,
        reply_markup=await create_regex_pagination_mp(name_list, page, has_more),
    )


@router.callback_query(F.data.startswith("next_page"))
async def next_page(callback: CallbackQuery, state: FSMContext, db: Database):
    await callback.answer()
    page = int(callback.data.split("|")[1])
    await state.update_data(page=page)

    phones, has_more = await db.phone.get_pagination(
        user_id=callback.from_user.id,
        offset=page * cfg.db.limit_phones,
        limit=cfg.db.limit_phones,
    )

    name_list = [phone.name for phone in phones]

    await callback.message.edit_text(
        BASES_LIST_MSG,
        reply_markup=await create_regex_pagination_mp(name_list, page, has_more),
    )


@router.callback_query(F.data.startswith("prev_page"))
async def prev_page(callback: CallbackQuery, state: FSMContext, db: Database):
    await callback.answer()
    page = int(callback.data.split("|")[1])
    await state.update_data(page=page)

    phones, has_more = await db.phone.get_pagination(
        user_id=callback.from_user.id,
        offset=page * cfg.db.limit_phones,
        limit=cfg.db.limit_phones,
    )

    name_list = [phone.name for phone in phones]

    await callback.message.edit_text(
        BASES_LIST_MSG,
        reply_markup=await create_regex_pagination_mp(name_list, page, has_more),
    )


@router.callback_query(F.data.startswith("phone_name"))
async def phone_name(callback: CallbackQuery, db: Database):
    await callback.answer()
    name = callback.data.split("|")[1]
    phone = await db.phone.get(user_id=callback.from_user.id, name=name)
    text = phone_base_click_msg(phone.name, phone.text)
    text = text.replace("end_of_text", "")
    await callback.message.edit_text(text, reply_markup=await create_phone_mp(name))


@router.callback_query(F.data.startswith("phone_edit_text"))
async def phone_edit_text(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    name = callback.data.split("|")[1]
    await state.set_state(EditPhoneBaseState.text)
    await state.update_data(name=name)

    await callback.message.delete()

    await callback.message.answer(
        ADD_PHONE_TEXT_MSG,
        reply_markup=cancel_mp,
    )


@router.callback_query(F.data.startswith("phone_edit_file"))
async def phone_edit_file(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    name = callback.data.split("|")[1]
    await state.set_state(EditPhoneBaseState.file)
    await state.update_data(name=name)

    await callback.message.delete()

    await callback.message.answer(ADD_CSV_MSG, reply_markup=cancel_mp)


@router.callback_query(F.data.startswith("phone_get"))
async def phone_get(callback: CallbackQuery, db: Database):
    await callback.answer()
    name = callback.data.split("|")[1]
    phone = await db.phone.get(user_id=callback.from_user.id, name=name)

    path_to_dir_user, path_to_file = await create_file_text(
        text=phone.numbers, name=name, user_id=callback.from_user.id
    )

    await callback.message.delete()

    await callback.message.answer_document(
        FSInputFile(path_to_file),
        reply_markup=start_mp,
    )

    shutil.rmtree(path_to_dir_user)


@router.callback_query(F.data.startswith("phone_link"))
async def phone_link(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    name = callback.data.split("|")[1]

    await state.set_state(GetLinksState.quantity)
    await state.update_data(name=name)

    await callback.message.delete()

    await callback.message.answer(GET_LINKS_MSG, reply_markup=cancel_mp)


@router.message(F.text, GetLinksState.quantity)
async def phone_link_quantity(
    message: Message, state: FSMContext, db: Database, bot: Bot
):
    try:
        quantity = int(message.text)
    except ValueError:
        await message.answer(GET_LINKS_WRONG_MSG, reply_markup=cancel_mp)
        return

    if quantity <= 0:
        await message.answer(GET_LINKS_WRONG_MSG, reply_markup=cancel_mp)
        return

    data = await state.get_data()
    name = data.get("name")
    page = data.get("page")

    phone = await db.phone.get(user_id=message.from_user.id, name=name)
    if len(phone.numbers.split("|")) <= phone.last_quantity:
        await state.clear()
        await message.answer(ALL_NUMBERS_SHOWED_MSG, reply_markup=start_mp)
        return

    text = await create_text_links(phone, quantity, phone.last_quantity)

    split_chunks = split_text(text)

    await state.clear()
    for chunk in split_chunks:
        try:
            chunk = chunk.replace("end_of_text", "")
            await message.answer(
                chunk,
                reply_markup=start_mp,
                disable_web_page_preview=True,
                parse_mode=ParseMode.HTML,
            )
        except Exception as e:
            logger.error(f"Error sending message link: {e}")
            continue
        # await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=msg.message_id, reply_markup=await copy_mp(msg.message_id))

    text = phone_base_click_msg(phone.name, phone.text)
    text = text.replace("end_of_text", "")

    await message.answer(text, reply_markup=await create_phone_mp(name, True))

    await db.phone.update_last_quantity(
        user_id=message.from_user.id, name=name, last_quantity=quantity
    )


@router.callback_query(F.data == "copy_text")
async def copy_text(callback: CallbackQuery, bot: Bot):
    text = callback.message.text

    ok = copy_text_to_clipboard(text, bot)
    if not ok:
        await callback.answer(COPY_TEXT_ERROR_MSG, show_alert=True)
        return

    await callback.answer(COPY_TEXT_SUCCESS_MSG)
