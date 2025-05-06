from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from pydantic import ValidationError

from bot.states import AuthStates
from bot.utils import password_manager

from database import db_manager, User
from common import ShortMessages, bot_logger


signup_r = Router()


@signup_r.message(Command('signup'))
async def signup(message: Message, state: FSMContext):

    telegram_id = message.from_user.id

    async with db_manager.session() as session:
        user = await User.get(session=session, field=User.telegram_id, value=telegram_id)

        if user:
            return await message.answer('you are already signed up')

    await state.set_state(AuthStates.name)

    username = message.from_user.username

    if username:
        return await message.answer(f'let\'s sign you up! enter your username (type "0" to keep "{username}"): ')
    else:
        return await message.answer(f'let\'s sign you up! enter your username:')


@signup_r.message(AuthStates.name)
async def get_name(message: Message, state: FSMContext):
    username = message.text

    if message.from_user.username:
        if username == '0':
            username = message.from_user.username

    if not username.replace(' ', '').isalpha():
        return await message.answer('username can only contain letters and spaces')
        
    if not (4 <= len(username) <= 32):
        return await message.answer('username length should be longer or equal to 4 symbols and shorter or equal to 32 symbols')

    async with db_manager.session() as session:
        user = await User.get(session=session, field=User.name, value=username)

        if user:
            return await message.answer('user with such username already exists. please choose another one')

    await state.update_data(username=username)
    await state.set_state(AuthStates.password)
    await message.answer('now, enter your password. there are no restrictions on the password, but make sure it is secure')


@signup_r.message(AuthStates.password)
async def get_password(message: Message, state: FSMContext):
    password = message.text

    await state.update_data(password=password)
    await message.delete()

    data = await state.get_data()
    username: str = data['username']
    password = data['password']
    telegram_id = message.from_user.id

    try:
        password = password_manager.hash_password(password)
    except AttributeError as er:
        print(er.name)

    async with db_manager.session() as session:
        await User.create(session=session, name=username, password=password, telegram_id=telegram_id)

    await message.answer('successfully signed up!')
    await state.clear()

    bot_logger.info(ShortMessages.USU)
