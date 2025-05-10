import aioredis

from src.config import REDIS_HOST, REDIS_PORT, REDIS_DB
    

redis_manager = aioredis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB
)
