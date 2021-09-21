import datetime

from sqlalchemy import Column, ForeignKey, Boolean, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    like = Column(Integer, index=True, default=0)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    owner = relationship("User", back_populates="items", lazy="subquery")
    comments = relationship("Comment", back_populates="item", lazy="subquery")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    item_id = Column(Integer, ForeignKey("items.id"))
    text = Column(String, index=True)

    owner = relationship("User", back_populates="comments", lazy="subquery")
    item = relationship("Item", back_populates="comments", lazy="subquery")
