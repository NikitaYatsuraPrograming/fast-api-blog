from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import UserCreate, User
from app.api.authorization.db import authenticate_user, get_user_by_email,\
    create_user_db
from app.api.authorization.schemas import Token, User
from app.db.database import get_session
from resource.global_ import ACCESS_TOKEN_EXPIRE_MINUTES
from resource.token import create_access_token, get_current_active_user

router = APIRouter()


@router.post("/create", response_model=User)
async def create_user(
        user: UserCreate,
        db: AsyncSession = Depends(get_session)
):
    db_user = await get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await create_user_db(db=db, user=user)


@router.post("/login", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_session)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/profile", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
