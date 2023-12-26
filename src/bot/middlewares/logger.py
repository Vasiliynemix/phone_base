from typing import Any, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from loguru import logger

from src.bot.structures.transfer_data import TransferData


class LoggerMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: TransferData,
    ) -> Any:
        text = await self.get_text(event)
        logger.info(f"{event.from_user.id} - {text}")
        return await handler(event, data)

    @staticmethod
    async def get_text(event: Message | CallbackQuery) -> str:
        if isinstance(event, Message):
            return event.text
        elif isinstance(event, CallbackQuery):
            return event.data
