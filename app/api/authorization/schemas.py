from pydantic import BaseModel
from typing import List, Optional
from ..item.schemas import Item


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None


class UserBase(BaseModel):
    email: str
    username: str


class User(UserBase):
    id: int
    is_active: Optional[bool] = None
    items: List[Item] = []

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: str
    password: str
