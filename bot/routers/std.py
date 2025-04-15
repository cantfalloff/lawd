from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database import User


std_r = Router()


@std_r.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    data = await state.get_data()
    user: User = data.get('user')

    await message.answer(f'hi, {user.name}!')
