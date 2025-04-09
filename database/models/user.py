from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from database.models.base import Base


class User(Base):
    name: Mapped[str] = mapped_column(String(32))
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()

    tags = relationship('Tag')
    sessions = relationship('Session', back_populates='user')

    telegram_id: Mapped[str] = mapped_column(nullable=True, index=True)
