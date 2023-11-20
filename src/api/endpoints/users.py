from typing import Any, List, Union
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from sqlalchemy import exc
from .dependencies import UOWDep
from src.dto.users import (
    UserDtoAdd,
    UserDtoDelete,
    UserDtoEdit,
    UserDtoGet,
    UserDtoRead,
    UserDtoResponse,
)
from src.crud.users import UsersService
from sqlalchemy.exc import NoResultFound

router = APIRouter()


@router.post("", response_model=Union[UserDtoResponse, Any])
async def add_user(
    uow: UOWDep,
    user: UserDtoAdd = Depends(UserDtoAdd.as_form),
) -> JSONResponse:
    try:
        user_id = await UsersService().add_user(uow, user)
        return {"user_id": user_id}
    except exc.IntegrityError:
        return JSONResponse(status_code=409, content={"error": "user already exist"})


@router.get("/all", response_model=Union[List[UserDtoRead], Any])
async def get_users(
    uow: UOWDep,
):
    users = await UsersService().get_users(uow)
    return users


@router.post("/one", response_model=Union[UserDtoRead, Any])
async def get_user(uow: UOWDep, user: UserDtoGet = Depends(UserDtoGet.as_form)):
    try:
        user = await UsersService().get_user(uow, user)
        return user
    except NoResultFound:
        return JSONResponse(status_code=404, content={"error": "user not found"})


@router.patch("", response_model=Union[UserDtoResponse, Any])
async def edit_user(
    uow: UOWDep,
    user: UserDtoEdit = Depends(UserDtoEdit.as_form),
):
    try:
        user_id = await UsersService().edit_user(uow, user)
        return {"id": user_id}
    except exc.NoResultFound:
        return JSONResponse(status_code=404, content={"User not Found": 404})


@router.delete("", response_model=Union[UserDtoResponse, Any])
async def delete_user(
    uow: UOWDep,
    user: UserDtoDelete = Depends(UserDtoDelete.as_form),
):
    try:
        user_id = await UsersService().delete_user(uow, user)
        return {"id": user_id}
    except exc.NoResultFound:
        return JSONResponse(status_code=404, content={"User not Found": 404})
