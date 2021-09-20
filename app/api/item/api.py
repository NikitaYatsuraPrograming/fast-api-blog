from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from resource.global_ import get_db
from resource.token import get_current_active_user
from .schemas import ItemCreate, Item, Comment, CommentCreate
from ..authorization.models import User
from .db import create_user_item, get_items_db, get_item_db, \
    create_comment_item, get_comments_db
from ..authorization.db import get_user

router = APIRouter()


@router.post("/create", response_model=Item)
async def create_items(
        item: ItemCreate,
        user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    db_item = create_user_item(db, item=item, user_id=user.id)
    if not db_item:
        raise HTTPException(status_code=400, detail="Not save item")
    owner = jsonable_encoder(db_item.owner)
    db_item = jsonable_encoder(db_item)
    db_item['owner'] = owner
    return db_item


@router.get("", response_model=List[Item])
async def get_items(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    update_items = []
    items = get_items_db(skip=skip, limit=limit, db=db)
    for item in items:
        owner = jsonable_encoder(item.owner)
        item = jsonable_encoder(item)
        item['owner'] = owner
        update_items.append(item)
    return update_items


@router.get("/{item_id}", response_model=Item)
async def get_item(
        item_id: int,
        db: Session = Depends(get_db)
):
    item = get_item_db(item_id=item_id, db=db)
    owner = jsonable_encoder(item.owner)
    item = jsonable_encoder(item)
    item['owner'] = owner

    return item


@router.post("/{item_id}/comments_create", response_model=Comment)
async def create_comment(
        item_id: int,
        comment: CommentCreate,
        user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    db_comment = create_comment_item(
        db,
        comment=comment,
        user_id=user.id,
        item_id=item_id
    )
    if not db_comment:
        raise HTTPException(status_code=400, detail="Not save comments")

    owner = jsonable_encoder(db_comment.owner)
    db_comment = jsonable_encoder(db_comment)
    db_comment['owner'] = owner
    return db_comment


@router.get("/{item_id}/comments", response_model=List[Comment])
async def get_comments(
        item_id: int,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    update_comments = []
    comments = get_comments_db(skip=skip, limit=limit, db=db, item_id=item_id)
    for comment in comments:
        owner = jsonable_encoder(comment.owner)
        comment = jsonable_encoder(comment)
        comment['owner'] = owner
        update_comments.append(comment)

    return update_comments
