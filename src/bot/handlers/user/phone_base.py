import shutil

from aiofiles import os
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from src.bot.handlers.funks import (
    get_list_random_text,
    get_file_text,
    check_file_text,
    create_file_text,
    create_text_links,
    split_text,
)
from src.bot.keyboards.start import start_mp
from src.bot.keyboards.user.inline.phone import create_phone_mp
from src.bot.keyboards.user.inline.phone_base import list_phone_base_mp
from src.bot.keyboards.user.inline.phone_list import (
    create_bookmarks_keyboard,
)
from src.bot.keyboards.user.reply.cancel import cancel_mp
from src.bot.keyboards.yes_no import yes_no_mp
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
    await message.answer("Отменено", reply_markup=start_mp)


@router.message(F.text == "📱Базы номеров")
async def phone_base(message: Message):
    await message.answer("Базы номеров", reply_markup=list_phone_base_mp)


@router.callback_query(F.data == "phone_base_list_back")
@router.callback_query(F.data == "phone_cancel")
async def phone_base_list_back(callback: Message):
    await callback.answer()
    await callback.message.edit_text("Список баз", reply_markup=list_phone_base_mp)


@router.callback_query(F.data == "phone_base_add")
async def phone_base_add(callback: Message, state: FSMContext):
    await callback.answer()
    await state.set_state(AddPhoneBaseState.csv)
    await callback.message.answer(
        "загрузите csv файл с базой номеров", reply_markup=cancel_mp
    )


@router.message(F.document, AddPhoneBaseState.csv)
@router.message(F.document, EditPhoneBaseState.file)
async def phone_base_csv(message: Message, state: FSMContext, db: Database, bot: Bot):
    if message.document.mime_type != "text/csv":
        await message.answer("Это не csv файл", reply_markup=cancel_mp)
        return

    file_id = message.document.file_id

    file_text = await get_file_text(bot, file_id)
    ok = check_file_text(file_text)
    if not ok:
        await message.answer(
            (
                "CSV файл не в нужном формате\n"
                "В нем не может быть ничего кроме номеров в одной колонке\n"
                "Номера в формате 7хххххххххх"
            ),
            reply_markup=cancel_mp,
        )
        return

    current_state = await state.get_state()
    if current_state == EditPhoneBaseState.file:
        data = await state.get_data()
        name = data.get("name")
        await db.phone.update_numbers(
            user_id=message.from_user.id, name=name, numbers=file_text
        )
        await state.clear()
        await message.answer("Файл обновлен", reply_markup=start_mp)
        return

    await state.update_data(file_id=file_id)
    await state.set_state(AddPhoneBaseState.name)

    phones = await db.phone.get_all(user_id=message.from_user.id)

    phones_text = ""
    if len(phones) > 0:
        phones_text += "\nСписок загруженные имен:\n"
        phones_text += "\n".join([phone.name for phone in phones])

    await message.answer(
        f"Введите название базы, оно должно быть уникальным{phones_text}",
        reply_markup=cancel_mp,
    )


@router.message(AddPhoneBaseState.csv)
async def phone_base_csv_not_document(message: Message):
    await message.answer(
        "Загрузите файл в csv формате с базой номеров", reply_markup=cancel_mp
    )


@router.message(F.text, AddPhoneBaseState.name)
async def phone_base_name(message: Message, state: FSMContext, db: Database):
    phone = await db.phone.get(user_id=message.from_user.id, name=message.text)
    if phone is not None:
        await message.answer(
            "База с таким название уже существует", reply_markup=cancel_mp
        )
        return

    if len(message.text) > 20:
        await message.answer(f"Название слишком длинное, символов должно быть не больше 20. Текущая длина {len(message.text)}", reply_markup=cancel_mp)
        return

    await state.update_data(name=message.text)
    await state.set_state(AddPhoneBaseState.text)
    await message.answer(
        "Введите текст. Формат:\n{Добрый день|Здравствуйте}!"
        " Вам пишет компания «Системы Безопасности»\n\n"
        "Мы занимаемся {продажей|реализацией} и {установкой|монтажом}"
        " видеонаблюдения и систем безопасности для коммерческой и частной недвижимости.\n\n"
        "Подскажите, интересно ли вам усилить безопасность вашего дома или бизнеса?\n\n"
        "Слова в шаблоне {...|...|...} будут выбираться рандомно для каждой ссылки.",
        reply_markup=cancel_mp,
    )


@router.message(F.text, AddPhoneBaseState.text)
@router.message(F.text, EditPhoneBaseState.text)
async def phone_base_text(message: Message, state: FSMContext, db: Database):
    matches = get_list_random_text(message.text)

    check_open = len(matches) == message.text.count("{")
    check_cancel = len(matches) == message.text.count("}")
    check_pipe = len(matches) <= message.text.count("|")

    if not check_open or not check_cancel or not check_pipe:
        text_template = "\n".join(matches)
        await message.answer(
            f"текст не соответствует шаблону.\n\nНайденные шаблоны:\n"
            f"{text_template}\n\nПроверьте текст и введите еще раз",
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
        await message.answer("Текст обновлен", reply_markup=start_mp)
        return

    await state.update_data(text=message.text)
    data = await state.get_data()
    name = data.get("name")
    text = data.get("text")

    await state.set_state(AddPhoneBaseState.end)

    await message.answer(
        (
            f"Настройки новой базы:\n"
            f"<b>Название:</b>\n{name}\n"
            f"<b>Текст:</b>\n{text}\n\n"
            f"Все верно?"
        ),
        reply_markup=yes_no_mp,
        parse_mode="HTML",
    )


@router.callback_query(F.data == "yes", AddPhoneBaseState.end)
async def phone_base_yes(callback: Message, state: FSMContext, bot: Bot, db: Database):
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
    await callback.message.answer("База добавлена", reply_markup=start_mp)


@router.callback_query(F.data == "no", AddPhoneBaseState.end)
async def phone_base_yes(callback: Message, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.answer("Отмена добавления новой базы", reply_markup=start_mp)


@router.callback_query(F.data == "phone_base_list")
async def phone_base_list(callback: Message, db: Database):
    await callback.answer()
    page = 0

    phones, has_more = await db.phone.get_pagination(
        user_id=callback.from_user.id, offset=page, limit=cfg.db.limit_phones
    )
    if len(phones) == 0:
        await callback.message.answer("Список баз пуст", reply_markup=start_mp)
        return

    name_list = [phone.name for phone in phones]

    await callback.message.edit_text(
        "Список баз",
        reply_markup=await create_bookmarks_keyboard(name_list, page, has_more),
    )


@router.callback_query(F.data.startswith("next_page"))
async def next_page(callback: Message, db: Database):
    await callback.answer()
    page = int(callback.data.split("|")[1])

    phones, has_more = await db.phone.get_pagination(
        user_id=callback.from_user.id,
        offset=page * cfg.db.limit_phones,
        limit=cfg.db.limit_phones,
    )

    name_list = [phone.name for phone in phones]

    await callback.message.edit_text(
        "Список баз",
        reply_markup=await create_bookmarks_keyboard(name_list, page, has_more),
    )


@router.callback_query(F.data.startswith("prev_page"))
async def prev_page(callback: Message, db: Database):
    await callback.answer()
    page = int(callback.data.split("|")[1])

    phones, has_more = await db.phone.get_pagination(
        user_id=callback.from_user.id,
        offset=page * cfg.db.limit_phones,
        limit=cfg.db.limit_phones,
    )

    name_list = [phone.name for phone in phones]

    await callback.message.edit_text(
        "Список баз",
        reply_markup=await create_bookmarks_keyboard(name_list, page, has_more),
    )


@router.callback_query(F.data.startswith("phone_name"))
async def phone_name(callback: Message, db: Database):
    await callback.answer()
    name = callback.data.split("|")[1]
    phone = await db.phone.get(user_id=callback.from_user.id, name=name)
    text = f"Название:\n{phone.name}\nтекст:\n{phone.text}\n\nЧто хотите сделать?"
    await callback.message.edit_text(text, reply_markup=await create_phone_mp(name))


@router.callback_query(F.data.startswith("phone_edit_text"))
async def phone_edit_text(callback: Message, state: FSMContext):
    await callback.answer()
    name = callback.data.split("|")[1]
    await state.set_state(EditPhoneBaseState.text)
    await state.update_data(name=name)

    await callback.message.delete()

    await callback.message.answer(
        "Введите текст. Формат:\n{Добрый день|Здравствуйте}!"
        " Вам пишет компания «Системы Безопасности»\n\n"
        "Мы занимаемся {продажей|реализацией} и {установкой|монтажом}"
        " видеонаблюдения и систем безопасности для коммерческой и частной недвижимости.\n\n"
        "Подскажите, интересно ли вам усилить безопасность вашего дома или бизнеса?\n\n"
        "Слова в шаблоне {...|...|...} будут выбираться рандомно для каждой ссылки.",
        reply_markup=cancel_mp,
    )


@router.callback_query(F.data.startswith("phone_edit_file"))
async def phone_edit_file(callback: Message, state: FSMContext):
    await callback.answer()
    name = callback.data.split("|")[1]
    await state.set_state(EditPhoneBaseState.file)
    await state.update_data(name=name)

    await callback.message.delete()

    await callback.message.answer(
        "Загрузите файл в csv формате с базой номеров", reply_markup=cancel_mp
    )


@router.callback_query(F.data.startswith("phone_get"))
async def phone_get(callback: Message, db: Database):
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
async def phone_link(callback: Message, state: FSMContext):
    await callback.answer()
    name = callback.data.split("|")[1]

    await state.set_state(GetLinksState.quantity)
    await state.update_data(name=name)

    await callback.message.delete()

    await callback.message.answer(
        "Введите количество ссылок, которые хотите получить", reply_markup=cancel_mp
    )


@router.message(F.text, GetLinksState.quantity)
async def phone_link_quantity(message: Message, state: FSMContext, db: Database):
    try:
        quantity = int(message.text)
    except ValueError:
        await message.answer(
            "Это не число, введите целое число > 0", reply_markup=cancel_mp
        )
        return

    if quantity <= 0:
        await message.answer("Введите целое число > 0", reply_markup=cancel_mp)
        return

    data = await state.get_data()
    name = data.get("name")

    phone = await db.phone.get(user_id=message.from_user.id, name=name)

    text = await create_text_links(phone, quantity)

    split_chunks = split_text(text)

    await state.clear()
    for chunk in split_chunks:
        await message.answer(
            chunk, reply_markup=start_mp, disable_web_page_preview=True, parse_mode="HTML"
        )
