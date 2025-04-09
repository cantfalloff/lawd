import uuid

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs

from database.db import Session_dp


class Base(AsyncAttrs, DeclarativeBase):

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'


    @classmethod
    async def create(cls, session: Session_dp, **kwargs):
        instance = cls(**kwargs)

        session.add(instance)
        await session.commit()

        return instance
