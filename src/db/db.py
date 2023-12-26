from typing import Any

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from src.db.repositories.phone import PhoneRepo
from src.db.repositories.user import UserRepo


def engine(url: URL | str, level: str) -> AsyncEngine:
    if level != "debug":
        level = None
    return create_async_engine(url=url, echo=level, pool_pre_ping=True)


def async_session_factory(bind: AsyncEngine) -> AsyncSession | Any:
    return async_sessionmaker(bind=bind, class_=AsyncSession, expire_on_commit=False)


class Database:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.user = UserRepo(session)
        self.phone = PhoneRepo(session)
