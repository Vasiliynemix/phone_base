from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from src.bot.filters.register import RegisterFilter
from src.bot.keyboards.start import start_mp
from src.bot.lexicon.kexicon import START_COMMAND_MSG

router = Router()


@router.message(CommandStart(), RegisterFilter())
async def start(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        await state.clear()
        await message.answer(START_COMMAND_MSG, reply_markup=start_mp)


@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        await state.clear()
        await message.answer(START_COMMAND_MSG, reply_markup=start_mp)
