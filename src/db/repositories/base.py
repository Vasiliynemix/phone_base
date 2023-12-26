import abc
from typing import TypeVar, Generic

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Base

AbstractModel = TypeVar("AbstractModel")


class Repository(Generic[AbstractModel]):
    type_model: type[Base]
    session: AsyncSession

    def __init__(self, type_model: type[Base], session: AsyncSession):
        self.type_model = type_model
        self.session = session

    @abc.abstractmethod
    async def new(self, *args, **kwargs) -> None:
        pass
