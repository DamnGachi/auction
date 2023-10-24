from fastapi import APIRouter
from fastapi.responses import JSONResponse

from sqlalchemy import exc
from .dependencies import UOWDep
from src.dto.users import UserDtoAdd, UserDtoEdit
from src.crud.users import UsersService


router = APIRouter()


@router.post("")
async def add_user(
    user: UserDtoAdd,
    uow: UOWDep,
):
    user_id = await UsersService().add_user(uow, user)
    return {"user_id": user_id}


@router.get("")
async def get_users(
    uow: UOWDep,
):
    users = await UsersService().get_users(uow)
    return users


@router.patch("")
async def edit_users(
    user: UserDtoEdit,
    uow: UOWDep,
):
    try:
        users = await UsersService().edit_user(uow, user)
        return users
    except exc.NoResultFound:
        return JSONResponse(status_code=404, content={"User not Found": 404})
