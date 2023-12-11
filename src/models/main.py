from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from src.dto.lots import LotDTORead
from src.dto.users import UserDTORead

from src.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column
import uuid

# from src.utils.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    balance: Mapped[float]

    def to_read_model(self) -> UserDTORead:
        return UserDTORead(
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

    def to_read_model(self) -> UserDTORead:
        return UserDTORead(
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
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    current_bet: Mapped[float] = mapped_column(nullable=True)
    closed_bet: Mapped[float] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now(), nullable=True)
    closed_at: Mapped[datetime] = mapped_column(nullable=True)

    def to_read_model(self) -> LotDTORead:
        return LotDTORead(
            id=self.id,
            title=self.title,
            description=self.description,
            start_bet=self.start_bet,
            winner_uid=self.winner_uid,
            is_active=self.is_active,
            current_bet=self.current_bet,
            created_at=self.created_at,
            updated_at=self.updated_at,
            closed_at=self.closed_at,
        )


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]


# class LotHistory(Base):
#     __tablename__ = "lots_history"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     lot_id: Mapped[str] = mapped_column(
#         ForeignKey("lot.id"), nullable=True, unique=True
#     )
#     closed_bet: Mapped[float] = mapped_column(nullable=True)
