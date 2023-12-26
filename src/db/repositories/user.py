from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.user import User
from src.db.repositories.base import Repository


class UserRepo(Repository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def new(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
        username: str,
    ):
        await self.session.merge(
            User(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
            )
        )
        await self.session.commit()

    async def get(self, user_id: int) -> User | None:
        stmt = select(User).where(User.user_id == user_id)
        return await self.session.scalar(stmt)

    async def get_by_chat_id(self, chat_id: int) -> User | None:
        stmt = select(User).where(User.user_id == str(chat_id))
        return await self.session.scalar(stmt)

    async def get_all_chats(self) -> Sequence[User]:
        stmt = select(User)
        chats = await self.session.scalars(stmt)
        return chats.all()
