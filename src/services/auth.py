from datetime import datetime, timedelta, UTC
from fastapi import HTTPException, Depends
from typing import Optional, Literal
from sqlalchemy import select,and_
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer

from src.repository.users import UsersRepository
from src.database.db import get_db
from src.database.models import User
from src.conf.config import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


class AuthService:

    def _create_token(
        self,
        data: dict,
        expires_delta: timedelta,
        token_type: Literal["access", "refresh"],
    ):
        to_encode = data.copy()
        now = datetime.now(UTC)
        expire = now + expires_delta
        to_encode.update({"exp": expire, "iat": now, "token_type": token_type})
        encoded_jwt = jwt.encode(
            to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM
        )
        return encoded_jwt

    async def create_access_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        if expires_delta:
            access_token = self._create_token(data, expires_delta, "access")
        else:
            access_token = self._create_token(
                data, timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES), "access"
            )
        return access_token

    async def create_refresh_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        if expires_delta:
            refresh_token = self._create_token(data, expires_delta, "refresh")
        else:
            refresh_token = self._create_token(
                data, timedelta(minutes=config.REFRESH_TOKEN_EXPIRE_MINUTES), "refresh"
            )
        return refresh_token

    async def get_current_user(
        self, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
    ):
        try:
            payload = jwt.decode(
                token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
            )
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

    async def verify_refresh_token(self, refresh_token: str, db: AsyncSession):
        try:
            payload = jwt.decode(
                refresh_token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
            )
            username: str = payload.get("sub")
            token_type: str = payload.get("token_type")
            if username is None or token_type != "refresh":
                return None
            stmt = select(User).where(and_(User.username == username, User.refresh_token == refresh_token)
                
            )
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()

            return user
        except JWTError:
            return None
