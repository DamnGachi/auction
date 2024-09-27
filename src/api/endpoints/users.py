from typing import Any, List, Union

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import exc
from sqlalchemy.exc import NoResultFound
from fastapi_pagination import Page, paginate
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


@router.get("/all", response_model=Union[List[UserDTORead], Any])
async def get_users(
    uow: UOWDep,
):
    users = await UsersService().get_users(uow)
    return paginate(users)


@router.post("/one", response_model=Union[UserDTORead, Any])
async def get_user(uow: UOWDep, user: UserDTOGet = Depends(UserDTOGet.as_form)):
    try:
        user = await UsersService().get_user(uow, user)
        return user
    except NoResultFound:
        return JSONResponse(status_code=404, content={"error": "User not found"})


@router.patch("", response_model=Union[UserDTOResponse, Any])
async def edit_user(
    uow: UOWDep,
    user: UserDTOEdit = Depends(UserDTOEdit.as_form),
):
    try:
        user_id = await UsersService().edit_user(uow, user)
        return {"id": user_id}
    except exc.NoResultFound:
        return JSONResponse(status_code=404, content={"error": "User not found"})


@router.delete("", response_model=Union[UserDTOResponse, Any])
async def delete_user(
    uow: UOWDep,
    user: UserDTODelete = Depends(UserDTODelete.as_form),
):
    user_id = await UsersService().delete_user(uow, user)
    print(user_id)
    if user_id is not None:
        return {"id": user_id}
    else:
        return JSONResponse(status_code=404, content={"error": "User not found"})
