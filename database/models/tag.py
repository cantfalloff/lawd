import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Tag(Base):
    title: Mapped[str] = mapped_column()
    icon: Mapped[str] = mapped_column(default='')

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))
    user = relationship('User', back_populates='tags')
