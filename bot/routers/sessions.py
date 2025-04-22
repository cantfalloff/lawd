import uuid
from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from sqlalchemy import select

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import db_manager, Tag, User, Session

from bot.views import is_active_session
from bot.keyboards import session_keyboard, break_keyboard


sessions_r = Router()


async def inline_tags(user: User):
    keyboard = InlineKeyboardBuilder()
    async with db_manager.session() as session:
        tags = await Tag.all_where(session=session, field=Tag.user_id, value=user.id)
    
    for t in tags:
        keyboard.add(InlineKeyboardButton(text=t.title + t.icon, callback_data=f'tag:{t.title}:{user.id}'))

    return keyboard.adjust(1).as_markup() if len(tags) > 0 else None


@sessions_r.message(Command('ss'))
async def start_session(message: Message, state: FSMContext):
    data = await state.get_data()
    user: User = data.get('user')

    await state.update_data(user=user)

    if await is_active_session(user_id=user.id):
        return await message.answer('you already started a session')

    keyboard = await inline_tags(user=user)

    if keyboard is None:
        return await message.answer('you do not have any tags yet. enter /add_tag to create one')

    return await message.answer('choose a tag to start your session', reply_markup=keyboard)


@sessions_r.callback_query(F.data.startswith('tag:'))
async def session(callback: CallbackQuery, state: FSMContext):
    tag_title = callback.data.split(':')[1]
    user_id = uuid.UUID(callback.data.split(':')[2])
    start_time = datetime.now()

    # check for existing sessions

    if await is_active_session(user_id=user_id):
        return await callback.message.edit_text('you already started a session')

    await state.update_data(start_time=start_time)

    async with db_manager.session() as session:
        stmt = select(Tag).where(Tag.user_id==user_id).where(Tag.title==tag_title)
        query = await session.execute(stmt)
        tag = query.scalars().first()
        await state.update_data(tag=tag)

        # register new session
        work_session = await Session.create(
            session=session, 
            start=start_time, 
            end=start_time, # end time = start time, because it cannot be None. it is just a temporary value
            breaks=0,
            description='', 
            tag_id=tag.id,
            user_id=user_id,
            is_active=True
        )

        await callback.message.edit_text(f'''
            \n{tag.title}{tag.icon}\nstart time: {start_time.year}-{start_time.month}-{start_time.day} {start_time.hour}:{start_time.minute}:{start_time.second}''', 
        parse_mode='HTML', reply_markup=session_keyboard)
    
    await callback.answer(f'you choose {tag_title}')


@sessions_r.callback_query(F.data == 'sk:finish_the_session')
async def finish_the_session(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user: User = data.get('user')
    end_time = datetime.now()
    breaks: int = data.get('break_seconds')

    async with db_manager.session() as _db_session:

        stmt = select(Session).where(Session.user_id==user.id).where(Session.is_active==True)
        query = await _db_session.execute(stmt)
        work_session = query.scalars().first()

        tag: Tag = await Tag.get(session=_db_session, field=Tag.id, value=work_session.tag_id)
        start_time: datetime = work_session.start

        # updating data
        work_session.end = end_time
        work_session.breaks = breaks if breaks else 0
        work_session.is_active = False

        await _db_session.commit()

    await state.clear()
    await callback.answer('the session has ended!')

    # work time info
    total_time = work_session.total_time
    hours = total_time // 3600
    total_time -= hours*3600
    minutes = total_time // 60
    total_time -= minutes * 60
    seconds = total_time

    work_info = f'you did <b>{tag.title}{tag.icon}</b> for '

    if hours != 0:
        work_info += f'<b>{hours}h</b> '

    if minutes != 0:
        work_info += f'<b>{minutes}m</b> '
    
    work_info += f'<b>{seconds}s</b>'

    # breaks time
    breaks = work_session.breaks
    bhours = breaks // 3600
    breaks -= bhours*3600
    bminutes = breaks // 60
    breaks -= bminutes * 60
    bseconds = breaks

    rest_info = f'you rested for '

    if breaks == 0:
        rest_info = 'you didn\'t rest during this session💪'
    else:
        if bhours != 0:
            rest_info += f'<b>{bhours}h</b> '

        if bminutes != 0:
            rest_info += f'<b>{bminutes}m </b>'
        
        rest_info += f'<b>{bseconds}s</b>'

    start_time_info = f'start time: {start_time.year}-{start_time.month}-{start_time.day} {start_time.hour}:{start_time.minute}:{start_time.second}'
    end_time_info = f'end time: {end_time.year}-{end_time.month}-{end_time.day} {end_time.hour}:{end_time.minute}:{end_time.second}'

    await callback.message.edit_text(f'the session has ended!\n\n{work_info}\n{rest_info}\n\n{start_time_info}\n{end_time_info}', parse_mode='HTML')


@sessions_r.callback_query(F.data == 'sk:make_a_break')
async def make_a_break(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_text('session is on break😴', reply_markup=break_keyboard)

    await state.update_data(break_start=datetime.now())


@sessions_r.callback_query(F.data == 'bk:continue')
async def continue_session(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user: User = data.get('user')

    start_time: datetime = data.get('start_time')
    break_start: datetime = data.get('break_start')

    
    break_seconds_1 = await state.get_value('break_seconds') # it is previous break duration
    break_seconds_1 = 0 if not break_seconds_1 else break_seconds_1

    break_seconds = (datetime.now() - break_start).seconds + break_seconds_1

    await state.update_data(break_seconds=break_seconds)

    async with db_manager.session() as _db_session:
        stmt = select(Session).where(Session.user_id==user.id).where(Session.is_active==True)
        query = await _db_session.execute(stmt)
        work_session = query.scalars().first()

        tag: Tag = await Tag.get(session=_db_session, field=Tag.id, value=work_session.tag_id)
        start_time: datetime = work_session.start

    await callback.message.edit_text(f'''
            \n{tag.title}{tag.icon}\nstart time: {start_time.year}-{start_time.month}-{start_time.day} {start_time.hour}:{start_time.minute}:{start_time.second}''', 
        parse_mode='HTML', reply_markup=session_keyboard)
