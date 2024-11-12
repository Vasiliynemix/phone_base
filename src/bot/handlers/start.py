from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from src.bot.filters.permission import PermissionFilter
from src.bot.filters.register import RegisterFilter
from src.bot.keyboards.start import start_mp
from src.bot.lexicon.lexicon import START_COMMAND_MSG

router = Router()

router.message.filter(PermissionFilter())
router.callback_query.filter(PermissionFilter())


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
