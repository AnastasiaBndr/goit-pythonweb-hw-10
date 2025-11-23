from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.users import UsersRepository
from src.security.hashing import Hash

hash_handler = Hash()


class UserService:

    def __init__(self, db: AsyncSession):
        self.repo = UsersRepository(db)

    async def register_user(self, username: str, password: str):
        exist = await self.repo.get_user_by_username(username)
        if exist:
            return None

        hashed = hash_handler.get_password_hash(password)
        return await self.repo.create_user(username, hashed)

    async def get_user_by_username(self, username: str):
        return await self.repo.get_user_by_username(username)
