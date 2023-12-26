from sqlalchemy import String, ForeignKey, BigInteger, UniqueConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models import Base


class Phone(Base):
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    numbers: Mapped[str] = mapped_column(Text, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
