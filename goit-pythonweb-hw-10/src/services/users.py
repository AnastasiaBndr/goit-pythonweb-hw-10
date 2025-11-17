from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.users import UsersRepository
from src.schemas import UserModel


class UserService:

    def __init__(self, db: AsyncSession) -> None:
        self.repository = UsersRepository(db)

    async def create_access_token(self, data: dict, expires_delta=None):
        return await self.repository.create_access_token(data, expires_delta)

    async def get_current_user(
        self, token: str, db: AsyncSession, credentials_exception
    ):
        return await self.repository.get_current_user(token, db, credentials_exception)
