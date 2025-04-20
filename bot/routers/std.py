from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database import User


std_r = Router() # this is the standart router, for commands like /info and other. notice: this router does NOT require an authentication
std_requiredauth_r = Router() # meanwhile, this router require authentication


@std_requiredauth_r.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    data = await state.get_data()
    user: User = data.get('user')

    await message.answer(f'hi, {user.name}!')


@std_r.message(Command('info'))
async def info(message: Message):
    with open('bot/routers/botinfo.txt', 'r') as file:
        text = file.read()


    return message.answer(text, 'HTML')
