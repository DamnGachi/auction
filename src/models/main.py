from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from src.dto.users import UserDtoRead

from src.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column
import uuid

# from src.utils.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    username: Mapped[str]
    hashed_password: Mapped[str]
    balance: Mapped[float]

    def to_read_model(self) -> UserDtoRead:
        return UserDtoRead(
            id=self.id,
            username=self.username,
            hashed_password=self.hashed_password,
            balance=self.balance,
        )


class UserLot(Base):
    __tablename__ = "users_lots"
    id: Mapped[int] = mapped_column(primary_key=True)
    lot_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("lots.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    def to_read_model(self) -> UserDtoRead:
        return UserDtoRead(
            id=self.id,
            lot_id=self.lot_id,
            user_id=self.user_id,
        )


class Lot(Base):
    __tablename__ = "lots"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    start_bet: Mapped[int] = mapped_column(nullable=False)
    winner_uid: Mapped[str] = mapped_column(
        ForeignKey("users.id"), nullable=True, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now())
    closed_at: Mapped[datetime]

    def to_read_model(self) -> UserDtoRead:
        return UserDtoRead(
            id=self.id,
            title=self.title,
            description=self.description,
            start_bet=self.start_bet,
            winner_uid=self.winner_uid,
            created_at=self.created_at,
            updated_at=self.updated_at,
            closed_at=self.closed_at,
        )


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]


class LotHistory(Base):
    __tablename__ = "lots_history"
    id: Mapped[int] = mapped_column(primary_key=True)
