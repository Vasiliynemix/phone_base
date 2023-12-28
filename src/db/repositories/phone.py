from sqlalchemy import select, Sequence, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.phone import Phone
from src.db.repositories.base import Repository


class PhoneRepo(Repository[Phone]):
    def __init__(self, session: AsyncSession):
        super().__init__(Phone, session)

    async def new(
        self,
        user_id: int,
        name: str,
        numbers: str,
        text: str,
    ):
        await self.session.merge(
            Phone(
                user_id=user_id,
                name=name,
                numbers=numbers,
                text=text,
            )
        )
        await self.session.commit()

    async def get(self, user_id: int, name: str) -> Phone | None:
        stmt = select(Phone).where(Phone.user_id == user_id).where(Phone.name == name)
        return await self.session.scalar(stmt)

    async def get_quantity(self, user_id: int, name: str, quantity: int) -> Sequence[Phone]:
        stmt = select(Phone).where(Phone.user_id == user_id).where(Phone.name == name).limit(quantity)
        phones = await self.session.scalars(stmt)
        return phones.all()

    async def get_all(self, user_id: int) -> Sequence[Phone]:
        stmt = select(Phone).where(Phone.user_id == user_id)
        phones = await self.session.scalars(stmt)
        return phones.all()

    async def get_pagination(
        self, user_id: int, offset: int, limit: int
    ) -> tuple[Sequence[Phone], bool]:
        stmt = (
            select(Phone)
            .where(Phone.user_id == user_id)
            .offset(offset)
            .limit(limit + 1)
            .order_by(Phone.created_at)
        )
        phones = await self.session.scalars(stmt)
        phone_list = phones.all()

        has_more = len(phone_list) > limit
        if has_more:
            phone_list = phone_list[:limit]

        return phone_list, has_more

    async def update_text(self, user_id: int, name: str, text: str):
        stmt = select(Phone).where(Phone.user_id == user_id).where(Phone.name == name)

        phone = await self.session.scalar(stmt)
        phone.text = text + "end_of_text"

        await self.session.commit()

    async def update_last_quantity(self, user_id: int, name: str, last_quantity: int):
        stmt = select(Phone).where(Phone.user_id == user_id).where(Phone.name == name)

        phone = await self.session.scalar(stmt)
        phone.last_quantity += last_quantity

        await self.session.commit()

    async def update_numbers(self, user_id: int, name: str, numbers: str):
        stmt = select(Phone).where(Phone.user_id == user_id).where(Phone.name == name)

        phone = await self.session.scalar(stmt)
        phone.numbers = numbers
        phone.last_quantity = 0

        await self.session.commit()

    async def delete(self, user_id: int, name: str):
        stmt = delete(Phone).where(Phone.user_id == user_id).where(Phone.name == name)

        await self.session.execute(stmt)

        await self.session.commit()
