import datetime

from sqlalchemy import Column, ForeignKey, Boolean, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    username = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner", lazy="joined")
    comments = relationship("Comment", back_populates="owner", lazy="joined")
