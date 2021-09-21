from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from resource.token import get_current_active_user
from .schemas import ItemCreate, Item, Comment, CommentCreate
from ..authorization.models import User
from .db import create_user_item, get_items_db, get_item_db, \
    create_comment_item, get_comments_db
from ...db.database import get_session

router = APIRouter()


@router.post("/create", response_model=Item)
async def create_items(
        item: ItemCreate,
        user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_session)
):
    db_item = await create_user_item(db, item=item, user_id=user.id)
    if not db_item:
        raise HTTPException(status_code=400, detail="Not save item")

    return db_item


@router.get("", response_model=List[Item])
async def get_items(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_session)
):

    items = await get_items_db(skip=skip, limit=limit, db=db)

    return items


@router.get("/{item_id}", response_model=Item)
async def get_item(
        item_id: int,
        db: AsyncSession = Depends(get_session)
):
    item = await get_item_db(item_id=item_id, db=db)

    return item


@router.post("/{item_id}/comments_create", response_model=Comment)
async def create_comment(
        item_id: int,
        comment: CommentCreate,
        user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_session)
):
    db_comment = await create_comment_item(
        db,
        comment=comment,
        user_id=user.id,
        item_id=item_id
    )
    if not db_comment:
        raise HTTPException(status_code=400, detail="Not save comments")

    return db_comment


@router.get("/{item_id}/comments", response_model=List[Comment])
async def get_comments(
        item_id: int,
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_session)
):
    comments = await get_comments_db(
        skip=skip,
        limit=limit,
        db=db,
        item_id=item_id
    )

    return comments
