from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from src.bot.filters.register import RegisterFilter
from src.bot.keyboards.start import start_mp

router = Router()


@router.message(CommandStart(), RegisterFilter())
async def start(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        await state.clear()
        await message.answer(f"Добро пожаловать в бота", reply_markup=start_mp)


@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        await state.clear()
        await message.answer("Добро пожаловать в бота", reply_markup=start_mp)
