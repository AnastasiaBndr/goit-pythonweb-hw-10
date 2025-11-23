from datetime import datetime, timedelta, UTC
from fastapi import HTTPException, Depends
from typing import Optional, Literal
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer

from src.repository.users import UsersRepository
from src.database.db import get_db

SECRET_KEY = "secret_key"
ALGORITHM = "HS256"
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 
ACCESS_TOKEN_EXPIRE_MINUTES = 15

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


class AuthService:

    def _create_token(
    data: dict, expires_delta: timedelta, token_type: Literal["access", "refresh"]
):
        to_encode = data.copy()
        now = datetime.now(UTC)
        expire = now + expires_delta
        to_encode.update({"exp": expire, "iat": now, "token_type": token_type})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def create_access_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        if expires_delta:
            access_token = self._create_token(data, expires_delta, "access")
        else:
            access_token = self._create_token(
                data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), "access"
            )
        return access_token

    async def get_current_user(
        self, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
    ):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid token")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        repo = UsersRepository(db)
        user = await repo.get_user_by_username(username)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user
