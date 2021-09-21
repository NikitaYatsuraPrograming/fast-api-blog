from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .models import Item, Comment
from .schemas import ItemCreate, CommentCreate
from ..authorization.models import User


def get_items_db(db: Session, skip: int = 0, limit: int = 100):
    items = db.query(Item).offset(skip).limit(limit).all()
    update_items = []

    for item in items:
        owner = jsonable_encoder(item.owner)
        item = jsonable_encoder(item)
        item['owner'] = owner
        update_items.append(item)

    return update_items


def get_item_db(db: Session, item_id: int):
    item = db.query(Item).filter(Item.id == item_id).first()
    owner = jsonable_encoder(item.owner)
    item = jsonable_encoder(item)
    item['owner'] = owner
    return item


def create_user_item(db: Session, item: ItemCreate, user_id: int):
    db_item = Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    owner = jsonable_encoder(db_item.owner)
    db_item = jsonable_encoder(db_item)
    db_item['owner'] = owner

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

    owner = jsonable_encoder(db_comment.owner)
    db_comment = jsonable_encoder(db_comment)
    db_comment['owner'] = owner

    return db_comment


def get_comments_db(db: Session, item_id: int, skip: int = 0, limit: int = 100):
    comments = db.query(Comment).filter(
        Comment.item_id == item_id
    ).offset(skip).limit(limit).all()
    update_comments = []

    for comment in comments:
        owner = jsonable_encoder(comment.owner)
        comment = jsonable_encoder(comment)
        comment['owner'] = owner
        update_comments.append(comment)
    return update_comments
