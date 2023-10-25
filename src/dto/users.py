from uuid import UUID
from fastapi import Form
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

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        hashed_password: str = Form(...),
        balance: float = Form(...),
    ):
        return cls(username=username, hashed_password=hashed_password, balance=balance)


class UserDtoEdit(BaseModel):
    id: UUID
    username: str | None
    hashed_password: str | None
    balance: float | None

    @classmethod
    def as_form(
        cls,
        id: UUID = Form(...),
        username: str = Form(...),
        hashed_password: str = Form(...),
        balance: float = Form(...),
    ):
        return cls(
            id=id, username=username, hashed_password=hashed_password, balance=balance
        )


class UserDtoGet(BaseModel):
    id: UUID
    username: str | None
    hashed_password: str | None
    balance: float | None

    @classmethod
    def as_form(
        cls,
        id: UUID = Form(...),
        username: str | None = Form(None),
        hashed_password: str | None = Form(None),
        balance: float | None = Form(None),
    ):
        return cls(
            id=id, username=username, hashed_password=hashed_password, balance=balance
        )


class UserDtoDelete(BaseModel):
    id: UUID

    @classmethod
    def as_form(
        cls,
        id: UUID = Form(...),
    ):
        return cls(id=id)
