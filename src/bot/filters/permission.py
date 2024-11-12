from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.config.config import cfg
from src.db.db import Database


class PermissionFilter(BaseFilter):
    async def __call__(self, message: Message, db: Database) -> bool:
        if message.from_user.id in cfg.bot.admins:
            return True

        user = await db.permission.get(user_id=message.from_user.id)
        if user is None:
            return False

        return True


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message, db: Database) -> bool:
        if message.from_user.id not in cfg.bot.admins:
            return False

        return True
