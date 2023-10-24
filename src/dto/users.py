from uuid import UUID
from pydantic import BaseModel


class UserDtoRead(BaseModel):
    id: UUID
    username: str
    balance: float

    class Config:
        from_attributes = True


class UserDtoAdd(BaseModel):
    id: UUID
    username: str
    hashed_password: str
    balance: float


class UserDtoEdit(BaseModel):
    id: UUID
    username: str | None
    hashed_password: str | None
    balance: float | None
