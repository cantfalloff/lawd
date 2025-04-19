import uuid
from datetime import datetime
from time import sleep

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from sqlalchemy import select

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import db_manager, Tag, User, Session


session_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='make a break', callback_data='sk:make_a_break')],
    [InlineKeyboardButton(text='finish the session', callback_data='sk:finish_the_session')]
])


break_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='continue', callback_data='bk:continue')],
    [InlineKeyboardButton(text='finish the session', callback_data='sk:finish_the_session')]
])


sessions_r = Router()


async def inline_tags(user: User):
    keyboard = InlineKeyboardBuilder()
    async with db_manager.session() as session:
        tags = await Tag.all_where(session=session, field=Tag.user_id, value=user.id)
    
    for t in tags:
        keyboard.add(InlineKeyboardButton(text=t.title + t.icon, callback_data=f'tag:{t.title}:{user.id}'))

    return keyboard.adjust(2).as_markup() if len(tags) > 0 else None


@sessions_r.message(Command('ss'))
async def start_session(message: Message, state: FSMContext):
    data = await state.get_data()
    user: User = data.get('user')

    await state.update_data(user=user)

    keyboard = await inline_tags(user=user)

    if keyboard is None:
        return await message.answer('you do not have any tags yet. enter /add_tag to create one')

    return await message.answer('choose a tag to start your session', reply_markup=keyboard)


@sessions_r.callback_query(F.data.startswith('tag:'))
async def session(callback: CallbackQuery, state: FSMContext):
    tag_title = callback.data.split(':')[1]
    user_id = uuid.UUID(callback.data.split(':')[2])
    start_time = datetime.now()

    await state.update_data(start_time=start_time)

    async with db_manager.session() as session:
        stmt = select(Tag).where(Tag.user_id==user_id).where(Tag.title==tag_title)
        query = await session.execute(stmt)
        tag = query.scalars().first()
        await state.update_data(tag=tag)

        await callback.message.edit_text(f'''
            \n{tag.title}{tag.icon}\nstart time: {start_time.year}-{start_time.month}-{start_time.day} {start_time.hour}:{start_time.minute}:{start_time.second}''', 
        parse_mode='HTML', reply_markup=session_keyboard)
    
    await callback.answer(f'you choose {tag_title}')


@sessions_r.callback_query(F.data == 'sk:finish_the_session')
async def finish_the_session(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    start_time = data.get('start_time')
    end_time = datetime.now()
    tag: Tag = data.get('tag')
    tag_id = tag.id
    user: User = data.get('user')
    user_id = user.id
    breaks: int = data.get('break_seconds')

    async with db_manager.session() as session:
        work_session = await Session.create(
            session=session, 
            start=start_time, 
            end=end_time,
            breaks=breaks, 
            description='', 
            tag_id=tag_id,
            # tag=tag,
            # user=user,
            user_id=user_id
        )

    await state.clear()
    await callback.answer('the session has ended!')

    total_time = work_session.total_time
    hours = total_time // 3600
    total_time -= hours*3600
    minutes = total_time // 60
    total_time -= minutes * 60
    seconds = total_time

    await callback.message.answer(f'session finished! you worked for <b>{hours}h {minutes}m {seconds}s</b>', parse_mode='HTML')


@sessions_r.callback_query(F.data == 'sk:make_a_break')
async def make_a_break(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_text('session is on break😴', reply_markup=break_keyboard)

    await state.update_data(break_start=datetime.now())


@sessions_r.callback_query(F.data == 'bk:continue')
async def continue_session(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    start_time: datetime = data.get('start_time')
    break_start: datetime = data.get('break_start')

    
    break_seconds_1 = await state.get_value('break_seconds') # it is previous break duration
    break_seconds_1 = 0 if not break_seconds_1 else break_seconds_1

    break_seconds = (datetime.now() - break_start).seconds + break_seconds_1

    await state.update_data(break_seconds=break_seconds)
    tag: Tag = data.get('tag')

    await callback.message.edit_text(f'''
            \n{tag.title}{tag.icon}\nstart time: {start_time.year}-{start_time.month}-{start_time.day} {start_time.hour}:{start_time.minute}:{start_time.second}''', 
        parse_mode='HTML', reply_markup=session_keyboard)
    