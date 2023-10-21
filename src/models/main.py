from uuid import uuid4
from src.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from sqlalchemy.types import JSON
from sqlalchemy.dialects.postgresql import JSONB

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    username: Mapped[str]
    categories: Mapped[JSONB] = mapped_column(JSON)
