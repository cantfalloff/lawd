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

        user_tg_id = event.from_user.id

        async with db_manager.session() as session:
            user = await User.get(session=session, field=User.telegram_id, value=user_tg_id)
            
            if not user:
                return event.answer('you are not authenticated. enter /signup to create a new account')
    
        return await handler(event, data)
