from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession


from src.database.models import User


class UsersRepository:

    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user_by_username(self, username: str):
        stmt = select(User).where(User.username == username)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, username: str, password: str):
        user = User(username=username, password=password)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
