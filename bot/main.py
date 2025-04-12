import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from .config import telegram_bot_token
from .routers import std_r
from .middleware import AuthMiddleware


bot = Bot(token=telegram_bot_token)
dp = Dispatcher(storage=MemoryStorage())

dp.message.middleware(AuthMiddleware())

dp.include_router(std_r)


if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
