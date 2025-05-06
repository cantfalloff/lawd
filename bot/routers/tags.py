from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from typing import Dict, Any

from bot.states import TagsCreationStates
from database import User, Tag, db_manager
from common import bot_logger, ShortMessages


tags_r = Router()


@tags_r.message(Command('my_tags', 'mytags'))
async def my_tags(message: Message, state: FSMContext):
    data = await state.get_data()
    user: User = data.get('user')

    async with db_manager.session() as session:
        tags = await Tag.all_where(session=session, field=Tag.user_id, value=user.id)

        return await message.answer(''.join(f'{t.title}{t.icon}\n' for t in tags) if tags else 'you do not have any tags yet. enter /add_tag to create one')


@tags_r.message(Command('add_tag', 'addtag'))
async def add_tag(message: Message, state: FSMContext):
    data = await state.get_data()
    user: User = data.get('user')

    await state.set_state(TagsCreationStates.title)
    await state.update_data(user=user)
    await message.answer('enter title for your tag: ')

    bot_logger.info(ShortMessages.CNT)


@tags_r.message(TagsCreationStates.title)
async def get_title(message: Message, state: FSMContext):
    title = message.text

    if not (len(title) <= 64):
        return await message.answer('title length should be less or equal to 64 symbols')

    await state.update_data(title=title)
    await state.set_state(TagsCreationStates.icon)
    await message.answer('enter icon for your tag, just for better view (type "0" if you do not want to add icon): ')


@tags_r.message(TagsCreationStates.icon)
async def get_icon(message: Message, state: FSMContext):
    icon = message.text

    if not (len(icon) <= 5):
        return await message.answer('icon length should be less or equal to 5')

    data = await state.get_data()
    title = data.get('title')
    user = data.get('user')

    async with db_manager.session() as session:
        tag = await Tag.create(session=session, user_id=user.id, title=title, icon=icon if icon != '0' else '')

    await message.answer('tag successfully created!')
    await state.clear()
