from typing import Any, List, Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import exc
from sqlalchemy.exc import NoResultFound

from src.crud.users import UsersService
from src.dto.users import (
    UserDTOAdd,
    UserDTODelete,
    UserDTOEdit,
    UserDTOGet,
    UserDTORead,
    UserDTOResponse,
)

from .dependencies import UOWDep

router = APIRouter()


@router.post("", response_model=Union[UserDTOResponse, Any])
async def add_user(
    uow: UOWDep,
    user: UserDTOAdd = Depends(UserDTOAdd.as_form),
) -> JSONResponse:
    try:
        user_id = await UsersService().add_user(uow, user)
        return {"user_id": user_id}
    except exc.IntegrityError:
        return JSONResponse(status_code=409, content={"error": "user already exist"})


@router.get("/all", response_model=Union[List[UserDTORead], Any])
async def get_users(
    uow: UOWDep,
):
    users = await UsersService().get_users(uow)
    return users


@router.post("/one", response_model=Union[UserDTORead, Any])
async def get_user(uow: UOWDep, user: UserDTOGet = Depends(UserDTOGet.as_form)):
    try:
        user = await UsersService().get_user(uow, user)
        return user
    except NoResultFound:
        return JSONResponse(status_code=404, content={"error": "user not found"})


@router.patch("", response_model=Union[UserDTOResponse, Any])
async def edit_user(
    uow: UOWDep,
    user: UserDTOEdit = Depends(UserDTOEdit.as_form),
):
    try:
        user_id = await UsersService().edit_user(uow, user)
        return {"id": user_id}
    except exc.NoResultFound:
        return JSONResponse(status_code=404, content={"User not Found": 404})


@router.delete("", response_model=Union[UserDTOResponse, Any])
async def delete_user(
    uow: UOWDep,
    user: UserDTODelete = Depends(UserDTODelete.as_form),
):
    try:
        user_id = await UsersService().delete_user(uow, user)
        return {"id": user_id}
    except exc.NoResultFound:
        return JSONResponse(status_code=404, content={"User not Found": 404})
