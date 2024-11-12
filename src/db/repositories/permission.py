from sqlalchemy import select, Sequence, delete, update, not_, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Permission
from src.db.repositories.base import Repository


class PermissionRepo(Repository[Permission]):
    def __init__(self, session: AsyncSession):
        super().__init__(Permission, session)

    async def new(
        self,
        user_id: int,
    ):
        await self.session.merge(
            Permission(
                user_id=user_id,
            )
        )
        await self.session.commit()

    async def get(self, user_id: int) -> Permission | None:
        stmt = select(Permission).where(Permission.user_id == user_id)
        return await self.session.scalar(stmt)

    async def get_all(self) -> list[Permission]:
        stmt = select(Permission)
        return list(await self.session.scalars(stmt))

    async def delete(self, user_id: int):
        stmt = delete(Permission).where(Permission.user_id == user_id)

        await self.session.execute(stmt)

        await self.session.commit()
