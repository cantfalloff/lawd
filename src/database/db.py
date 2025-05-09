from typing import AsyncIterator, Annotated
import contextlib

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncConnection,
    AsyncSession,
    AsyncEngine
)
from fastapi import Depends

from src.common import db_logger


class DatabaseManager:

    def __init__(self):
        self._sessionmaker: async_sessionmaker | None = None
        self._engine: AsyncEngine | None = None


    def init(self, host: str, echo: bool = False):
        try:
            self._engine = create_async_engine(host, echo=echo)
            self._sessionmaker = async_sessionmaker(
                autocommit=False,
                expire_on_commit=False,
                bind=self._engine
            )

            db_logger.info('database initialized')

        except Exception as _:
            db_logger.error('database error', exc_info=True)


    async def close(self):
        try:
            await self._engine.dispose()

            self._engine = None
            self._sessionmaker = None

            db_logger.info('database closed')
        except Exception as _:
            db_logger.error('database error', exc_info=True)


    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                db_logger.error('database error', exc_info=True)
                raise


    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        session = self._sessionmaker()

        try:
            yield session
        except Exception:
            await session.rollback()
            db_logger.critical('exception', exc_info=True)
            raise
        finally:
            await session.close()


db_manager = DatabaseManager()


async def get_db_session():
    async with db_manager.session() as session:
        db_logger.info('yield session')
        yield session


Session_dp = Annotated[AsyncSession, Depends(get_db_session)]
