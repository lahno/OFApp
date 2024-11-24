from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import Mapped

from db.database import Base, int_pk


class MessageORM(Base):
    __tablename__ = "messages"

    id: Mapped[int_pk] = Column(Integer, primary_key=True)
    message = Column(String(256), nullable=False, unique=True)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class AccountORM(Base):
    __tablename__ = "accounts"

    id: Mapped[int_pk] = Column(Integer, primary_key=True)
    email = Column(String(55), nullable=False, unique=True)
    password = Column(String(55), nullable=True)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int_pk] = Column(Integer, primary_key=True)
    username = Column(String(55), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
