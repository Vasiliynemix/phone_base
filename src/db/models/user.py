from sqlalchemy import BigInteger, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.db.models import Base


class User(Base):
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
