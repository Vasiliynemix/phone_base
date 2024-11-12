from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.bot.filters.permission import AdminFilter
from src.bot.keyboards.start import start_mp
from src.bot.lexicon.lexicon import START_COMMAND_MSG, VALUE_ERROR_MSG, ACCESS_SUCCESS_MSG, ACCESS_COMMAND_MSG
from src.db.db import Database

router = Router()

router.message.filter(AdminFilter())
router.callback_query.filter(AdminFilter())


@router.message(Command(commands=["users"]))
async def users_handle(message: types.Message, db: Database):
    if message.chat.type == "private":
        users = await db.permission.get_all()
        await message.answer(ACCESS_COMMAND_MSG + ", ".join([str(user.user_id) for user in users]), reply_markup=start_mp)


@router.message(Command(commands=["add_users"]))
async def add_users_handle(message: types.Message, db: Database):
    if message.chat.type == "private":
        user_id = message.text.split(" ")[1]
        try:
            user_id = int(user_id)
        except ValueError:
            await message.answer(VALUE_ERROR_MSG, reply_markup=start_mp)
            return

        user_check = await db.permission.get(user_id=user_id)
        if user_check is None:
            await db.permission.new(user_id=user_id)

        await message.answer(ACCESS_SUCCESS_MSG, reply_markup=start_mp)


@router.message(Command(commands=["del_users"]))
async def del_users_handle(message: types.Message, db: Database):
    if message.chat.type == "private":
        user_id = message.text.split(" ")[1]
        try:
            user_id = int(user_id)
        except ValueError:
            await message.answer(VALUE_ERROR_MSG, reply_markup=start_mp)
            return

        await db.permission.delete(user_id=user_id)
        await message.answer(ACCESS_SUCCESS_MSG, reply_markup=start_mp)
