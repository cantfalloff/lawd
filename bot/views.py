from sqlalchemy import select

from database import db_manager, Session


async def is_active_session(user_id):
    '''
    this function takes user's id and checks his active sessions. if there's one - raise `ActiveSessionException`.
    it means that user already started a session, so he cannot start another one.

    if there is an active session - returns `True`, else - `False`
    '''

    async with db_manager.session() as session:
        # check for existing sessions

        stmt = select(Session).where(Session.user_id==user_id).where(Session.is_active==True)
        query = await session.execute(stmt)
        active_session = query.scalars().first()

        return True if active_session else False
