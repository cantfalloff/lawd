import os

from dotenv import load_dotenv

from src.common import root_logger
from src.exceptions import NoneValueInConfig


load_dotenv(override=True)

''' rewrite `os.getenv` method to add one feature: now it will automatically check for `None` (danger!) values'''
def getenv_(key, default=None):
    """Get an environment variable, return None if it doesn't exist.
    The optional second argument can specify an alternate default.
    key, default and the result are str."""

    env_value = os.environ.get(key, default)

    if env_value is None:
        root_logger.critical(f'None value in config file: {key}')

        raise NoneValueInConfig(f'None value in config file: {key}')

    return env_value


DATABASE_USER=getenv_('database_user'),
DATABASE_PASSWORD=getenv_('database_password'),
DATABASE_HOST=getenv_('database_host'),
DATABASE_NAME=getenv_('database_name'),
DATABASE_PORT=getenv_('database_port')

DATABASE_URL = f'postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
API_KEY = getenv_('api_key')
