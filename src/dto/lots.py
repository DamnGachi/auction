from uuid import UUID
from fastapi import Form
from pydantic import BaseModel


class LotDtoRead(BaseModel):
    id: UUID
    title: str
    start_bet: int
    description: str

    class Config:
        from_attributes = True


class LotDtoAdd(BaseModel):
    id: UUID
    title: str
    start_bet: int
    description: str

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        description: str = Form(...),
        start_bet: int = Form(...),
    ):
        return cls(title=title, start_bet=start_bet)


class LotDtoEdit(BaseModel):
    id: UUID
    title: str | None
    start_bet: int | None

    @classmethod
    def as_form(
        cls,
        id: UUID = Form(...),
        title: str = Form(...),
        start_bet: int = Form(...),
    ):
        return cls(
            id=id, title=title, start_bet=start_bet
        )


class LotDtoGet(BaseModel):
    id: UUID
    title: str | None
    start_bet: int | None

    @classmethod
    def as_form(
        cls,
        id: UUID = Form(...),
        title: str | None = Form(None),
        start_bet: int | None = Form(None),
    ):
        return cls(
            id=id, title=title, start_bet=start_bet
        )


class LotDtoDelete(BaseModel):
    id: UUID

    @classmethod
    def as_form(
        cls,
        id: UUID = Form(...),
    ):
        return cls(id=id)
