from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from src.bot.filters.permission import PermissionFilter
from src.bot.lexicon.lexicon import NOT_ACCESS_MSG

router = Router()


@router.message(~PermissionFilter())
async def other_handle(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        await state.clear()
        await message.answer(NOT_ACCESS_MSG, reply_markup=None)


@router.callback_query(~PermissionFilter())
async def other_handle(callback: types.CallbackQuery, state: FSMContext):
    if callback.chat.type == "private":
        await state.clear()
        await callback.message.delete_reply_markup()
        await callback.message.answer(NOT_ACCESS_MSG, reply_markup=None)
