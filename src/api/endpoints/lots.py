from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy import exc

from src.dto.lots import LotDtoAdd
from .dependencies import UOWDep
from src.dto.users import UserDtoAdd, UserDtoDelete, UserDtoEdit, UserDtoGet
from src.crud.users import UsersService


router = APIRouter()


@router.get("/")
async def add_lot(
    uow: UOWDep,
    user: LotDtoAdd = Depends(LotDtoAdd.as_form),
):
    user_id = await UsersService().add_user(uow, user)
    return {"user_id": user_id}
