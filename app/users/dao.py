from app.dao.base import BaseDAO
from app.users.models import User
from sqlalchemy import select
from app.database import async_session_maker

class UsersDAO(BaseDAO):
    model = User
    
    @classmethod
    async def find_one_or_none_by_id(cls, data_id: str):  # str вместо int
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
    
    @classmethod
    async def find_one_or_none_by_email(cls, email: str):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(email=email)
            result = await session.execute(query)
            return result.scalar_one_or_none()