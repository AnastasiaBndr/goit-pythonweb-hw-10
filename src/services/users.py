from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.users import UsersRepository
from src.security.hashing import Hash
from src.schemas import UserModel

hash_handler = Hash()


class UserService:

    def __init__(self, db: AsyncSession):
        self.repo = UsersRepository(db)

    async def register_user(self, body:UserModel):
        exist = await self.repo.get_user_by_username(body.username)
        if exist:
            return None

        hashed = hash_handler.get_password_hash(body.password)
        return await self.repo.create_user(body.username, hashed)

    async def get_user_by_id(self, user_id: int):
        return await self.repo.get_user_by_id(user_id)

    async def get_user_by_username(self, username: str):
        return await self.repo.get_user_by_username(username)
