from typing import TypedDict

from sqlalchemy.ext.asyncio import AsyncEngine

from pkg.logger import Logger
from src.db.db import Database


class TransferData(TypedDict):
    engine: AsyncEngine
    db: Database
    log: Logger
