import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from .config import telegram_bot_token
from .routers import std_r, signup_r, tags_r, sessions_r, std_requiredauth_r
from .middleware import AuthMiddleware


bot = Bot(token=telegram_bot_token)
dp = Dispatcher(storage=MemoryStorage())


dp.include_routers(std_r, std_requiredauth_r, signup_r, tags_r, sessions_r)

# include AuthMiddleware

std_requiredauth_r.message.middleware(AuthMiddleware())
tags_r.message.middleware(AuthMiddleware())
sessions_r.message.middleware(AuthMiddleware())
sessions_r.callback_query.middleware(AuthMiddleware())


commands = [
    BotCommand(command='ss', description='start session'),
    BotCommand(command='signup', description='create a new account'),
    BotCommand(command='addtag', description='create a new tag'),
    BotCommand(command='mytags', description='see all of my tags')
]


async def run():
    await bot.set_my_commands(commands=commands)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(run())
