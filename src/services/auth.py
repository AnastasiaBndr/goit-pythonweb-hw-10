from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from src.repository.users import UsersRepository

SECRET_KEY = "secret_key"
ALGORITHM = "HS256"


class AuthService:

    def __init__(self, db: AsyncSession):
        self.repo = UsersRepository(db)

    async def create_access_token(self, data: dict, expires_delta=None):
        to_encode = data.copy()
        expire = (
            datetime.now(UTC) + timedelta(seconds=expires_delta)
            if expires_delta
            else datetime.now(UTC) + timedelta(minutes=15)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    async def get_current_user(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise HTTPException(
                    status_code=401, detail="Invalid authentication credentials"
                )
        except JWTError:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )

        return await self.repo.get_user_by_username(username)
