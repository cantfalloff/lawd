from datetime import datetime
import uuid

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Session(Base):
    start: Mapped[datetime] = mapped_column(DateTime)
    end: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    breaks: Mapped[int] = mapped_column(default=0)
    productivity_rate: Mapped[int] = mapped_column()

    tag_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('tags.id'))
    tag = relationship('Tag')

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))
    user = relationship('User', back_populates='sessions')

    @property
    def total_time(self) -> int:
        return (self.end - self.start).seconds - self.breaks
