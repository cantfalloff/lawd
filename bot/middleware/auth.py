from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.filters import Command
from typing import Callable, Dict, Any, Awaitable

from database.db import db_manager
from database.models import User


class AuthMiddleware(BaseMiddleware):
    '''
    checks user's authentications status.
    '''

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        user_tg_id = event.chat.id

        async with db_manager.session() as session:
            user = await User.get(session=session, field=User.telegram_id, value=user_tg_id)
            
            if not user:
                username = event.chat.username
                user = await User.create(session=session, name=username, telegram_id=user_tg_id)

                print(f'new user: {user.name}')
    
        result = await handler(event, data)

        return result
