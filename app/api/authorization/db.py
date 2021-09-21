from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from resource.global_ import pwd_context
from .schemas import UserCreate
from .models import User
from sqlalchemy.future import select


def verify_password(plain_password, hashed_password):
    print("@###" *10, pwd_context.verify(plain_password, hashed_password))
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))

    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))

    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))

    return result.scalars().first()


async def create_user_db(db: AsyncSession, user: UserCreate):
    db_user = User(
        email=user.email,
        password=get_password_hash(user.password),
        username=user.username
    )
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
    except IntegrityError as ex:
        await db.rollback()
    else:
        return db_user


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db=db, username=username)
    if not user:
        return False
    if not verify_password(plain_password=password,
                           hashed_password=user.password):
        return False
    return user
