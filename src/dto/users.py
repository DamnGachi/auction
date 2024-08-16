from uuid import UUID

from fastapi import Form
from pydantic import BaseModel


class UserDTORead(BaseModel):
    id: UUID
    username: str
    balance: float

    class Config:
        from_attributes = True


class UserDTOResponse(BaseModel):
    id: UUID

    class Config:
        from_attributes = True


class UserDTOAdd(BaseModel):
    # id: UUID
    username: str
    password: str
    balance: float

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        password: str = Form(...),
        balance: float = Form(...),
    ):
        return cls(username=username, password=password, balance=balance)


class UserDTOEdit(BaseModel):
    id: UUID
    username: str | None
    password: str | None
    balance: float | None

    @classmethod
    def as_form(
        cls,
        id: UUID = Form(...),
        username: str | None = Form(None),
        password: str | None = Form(None),
        balance: float | None = Form(None),
    ):
        return cls(
            id=id, username=username, password=password, balance=balance
        )


class UserDTOGet(BaseModel):
    id: UUID

    @classmethod
    def as_form(
        cls,
        id: UUID = Form(...),
    ):
        return cls(id=id)


class UserDTODelete(BaseModel):
    id: UUID

    @classmethod
    def as_form(
        cls,
        id: UUID = Form(...),
    ):
        return cls(id=id)
