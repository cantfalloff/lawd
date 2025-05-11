from fastapi import APIRouter, Request, status, HTTPException
from sqlalchemy import select

from src.common import api_logger
from src.database import Session_dp, User
from src.api.dependencies import api_key_dp
from src.schemas import UserSchema
from src.cache.redis_manager import redis_manager


auth_r = APIRouter(prefix='/auth', dependencies=[api_key_dp])


@auth_r.post('/signup')
async def signup(request: Request, session: Session_dp, user_data: UserSchema):

    # check for any user with the same name (because it should be unique)
    query = await session.execute(select(User).where(User.name==user_data.name))
    user = query.scalars().first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with such username already exists. please, try another one'
        )

    user = await User.create(
        session=session, 
        name=user_data.name,
        password=user_data.password, # it arrives already hashed, so i do not do it here
        telegram_id=user_data.telegram_id
    )

    # add new user to cache (in Redis) to mark them as registrated
    async with redis_manager.pipeline(transaction=True) as pipe:
        await pipe.rpush('users', f'{user_data.telegram_id}')
        await pipe.hset(f'{user_data.telegram_id}', key='name', value=user_data.name)

        await pipe.execute()

    api_logger.info(f'New user signed up: {user_data.name}')

    return {
        'status': status.HTTP_200_OK,
        'detail': 'successfully signed up!',
    }
