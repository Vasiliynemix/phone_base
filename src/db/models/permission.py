from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models import Base


class Permission(Base):
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
