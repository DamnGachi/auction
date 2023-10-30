from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy import exc
from .dependencies import UOWDep
from src.dto.users import UserDtoAdd, UserDtoDelete, UserDtoEdit, UserDtoGet
from src.crud.users import UsersService


router = APIRouter()


@router.post("")
async def add_user(
    user: UserDtoAdd,
    uow: UOWDep,
):
    user_id = await UsersService().add_user(uow, user)
    return {"user_id": user_id}


@router.get("/all")
async def get_users(
    uow: UOWDep,
):
    users = await UsersService().get_users(uow)
    return users


@router.post("/one")
async def get_user(uow: UOWDep, user: UserDtoGet):
    user = await UsersService().get_user(uow, user)
    return user


@router.patch("")
async def edit_user(
    user: UserDtoEdit,
    uow: UOWDep,
):
    try:
        users = await UsersService().edit_user(uow, user)
        return users
    except exc.NoResultFound:
        return JSONResponse(status_code=404, content={"User not Found": 404})


@router.delete("")
async def delete_user(
    user: UserDtoDelete,
    uow: UOWDep,
):
    try:
        users = await UsersService().delete_user(uow, user)
        return users
    except exc.NoResultFound:
        return JSONResponse(status_code=404, content={"User not Found": 404})
