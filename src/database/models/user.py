from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import BIGINT

from database.models.base import Base


class User(Base):
    name: Mapped[str] = mapped_column(String(32), unique=True)
    password: Mapped[str] = mapped_column()

    tags: Mapped[list['Tag']] = relationship('Tag')
    sessions: Mapped[list['Session']] = relationship('Session', back_populates='user')

    telegram_id: Mapped[int] = mapped_column(BIGINT, nullable=True, index=True)
