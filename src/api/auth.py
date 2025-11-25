from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import UserCreate
from src.database.db import get_db
from src.services.users import UserService
from src.services.auth import AuthService
from src.security.hashing import Hash
from src.schemas import TokenModel, TokenRefreshRequest

router = APIRouter(prefix="/auth", tags=["auth"])
hash_handler = Hash()
auth_service = AuthService()


@router.post("/register")
async def register(body: UserCreate, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)

    user = await user_service.get_user_by_username(body.username)
    if user:
        raise HTTPException(status_code=409, detail="Account already exists")

    new_user = await user_service.register_user(body)

    return {"username": new_user.username}


@router.post("/login")
async def login(
    form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    user = await user_service.get_user_by_username(form.username)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username")

    if not hash_handler.verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password")

    access_token = await auth_service.create_access_token({"sub": user.username})
    refresh_token = await auth_service.create_refresh_token({"sub": user.username})
    user.refresh_token = refresh_token
    await db.commit()
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh-token", response_model=TokenModel)
async def new_token(request: TokenRefreshRequest, db: AsyncSession = Depends(get_db)):
    user = await auth_service.verify_refresh_token(request.refresh_token, db)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token",
        )
    new_access_token = await auth_service.create_access_token(
        data={"sub": user.username}
    )
    return {
        "access_token": new_access_token,
        "refresh_token": request.refresh_token,
        "token_type": "bearer",
    }
