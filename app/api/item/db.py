from sqlalchemy.orm import Session

from .models import Item, Comment
from .schemas import ItemCreate, CommentCreate
from ..authorization.models import User


def get_items_db(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()


def get_item_db(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()


def create_user_item(db: Session, item: ItemCreate, user_id: int):
    db_item = Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_comment_item(
        db: Session,
        comment: CommentCreate,
        user_id: int,
        item_id: int
):
    db_comment = Comment(**comment.dict(), owner_id=user_id, item_id=item_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments_db(db: Session, item_id: int, skip: int = 0, limit: int = 100):
    return db.query(Comment).filter(
        Comment.item_id == item_id
    ).offset(skip).limit(limit).all()
