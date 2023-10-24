from uuid import UUID
from pydantic import BaseModel


class UserDtoRead(BaseModel):
    id: UUID
    username: str
    balance: float

    class Config:
        from_attributes = True


class UserDtoAdd(BaseModel):
    id: str
    username: str
    hashed_password: str
    balance: float
