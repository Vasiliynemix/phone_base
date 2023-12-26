from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.db.db import Database


class RegisterFilter(BaseFilter):
    async def __call__(self, message: Message, db: Database) -> bool:
        user = await db.user.get(user_id=message.from_user.id)
        if user is not None:
            return False
        await db.user.new(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
        )
        return True
