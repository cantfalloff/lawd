from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import DATABASE_URL
from src.common import api_logger
from src.database import db_manager
from .dependencies import api_key_dp


@asynccontextmanager
async def api_lifespan(app: FastAPI):
    api_logger.info('api started')
    db_manager.init(DATABASE_URL, echo=False)

    yield
    await db_manager.close()


app = FastAPI(
    title='thatrack',
    description='an application for tracking study and work time',
    dependencies=[api_key_dp],
    lifespan=api_lifespan
)
