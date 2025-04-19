import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Tag(Base):
    title: Mapped[str] = mapped_column(String(64))
    icon: Mapped[str] = mapped_column(String(5), default='')

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))
    user = relationship('User', back_populates='tags')
