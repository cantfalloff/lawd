import os

from dotenv import load_dotenv


load_dotenv(override=True)

database_url: str = 'postgresql+asyncpg://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}'.format(
    database_user=os.getenv('database_user'),
    database_password=os.getenv('database_password'),
    database_host=os.getenv('database_host'),
    database_name=os.getenv('database_name'),
    database_port=os.getenv('database_port')
)
