import uuid

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import select

from src.database.db import Session_dp
from src.common import db_logger


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


    @classmethod
    async def get(cls, session: Session_dp, field, value):
        stmt = select(cls).where(field == value)
        elem = await session.execute(stmt)

        elem = elem.scalars().first()

        return elem
    

    @classmethod
    async def all_where(cls, session: Session_dp, field, value):
        '''
        returns all objects by condition
        '''

        stmt = select(cls).where(field == value)
        elem = await session.execute(stmt)

        elem = elem.scalars().all()

        return elem
