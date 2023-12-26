from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from src.bot.structures.transfer_data import TransferData
from src.db.db import Database, async_session_factory


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: TransferData,
    ) -> Any:
        async_session = async_session_factory(bind=data["engine"])
        async with async_session() as session:
            data["db"] = Database(session)
            return await handler(event, data)
