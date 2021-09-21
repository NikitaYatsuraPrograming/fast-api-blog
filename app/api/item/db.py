from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import join

from .models import Item, Comment
from .schemas import ItemCreate, CommentCreate


async def get_items_db(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Item).offset(skip).limit(limit))

    return result.scalars().all()


async def get_item_db(db: AsyncSession, item_id: int):
    result = await db.execute(select(Item).filter(Item.id == item_id))
    return result.scalars().first()


async def create_user_item(db: AsyncSession, item: ItemCreate, user_id: int):
    db_item = Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    try:
        await db.commit()
        await db.refresh(db_item)
    except IntegrityError as ex:
        await db.rollback()
    else:
        return db_item


async def create_comment_item(
        db: AsyncSession,
        comment: CommentCreate,
        user_id: int,
        item_id: int
):
    db_comment = Comment(**comment.dict(), owner_id=user_id, item_id=item_id)
    db.add(db_comment)
    try:
        await db.commit()
        await db.refresh(db_comment)
    except IntegrityError as ex:
        await db.rollback()
    else:
        return db_comment


async def get_comments_db(db: AsyncSession, item_id: int, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Comment).filter(
        Comment.item_id == item_id
    ).offset(skip).limit(limit))

    return result.scalars().all()
