from pydantic import BaseModel, Field, Json
from datetime import datetime
from typing import List, Optional


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class OwnerItem(BaseModel):
    username: str
    create_date: Optional[datetime]

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    owner_id = int
    owner: OwnerItem
    create_date: Optional[datetime]

    class Config:
        orm_mode = True


class Item(ItemBase):
    id: int
    create_date: Optional[datetime]
    owner_id: int
    owner: OwnerItem
    comments: List[Comment]

    class Config:
        orm_mode = True
