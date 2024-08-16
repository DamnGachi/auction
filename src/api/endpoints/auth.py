from typing import Any, Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from src.crud.users import UsersService
from src.app.basic import JWTBearer
from src.repositories.auth import AuthRepository
from src.db.database import async_get_session
from src.dto.auth import (
    ProtectedResponse,
    TokenLoginResponse,
    TokenRefreshResponse,
    UserLoginDTO,
)
from src.dto.users import UserDTOAdd, UserDTORead
from .dependencies import UOWDep
from fastapi.responses import JSONResponse
from sqlalchemy import exc

router = APIRouter()


@router.post(
    "/register",
    response_model=Union[UserDTORead, Any],
)
async def register(
    uow: UOWDep,
    user: UserDTOAdd = Depends(UserDTOAdd.as_form),
) -> dict:
    try:
        user_id = await UsersService().add_user(uow, user)
        return {"user_id": user_id}
    except exc.IntegrityError:
        return JSONResponse(status_code=409, content={"error": "user already exist"})


@router.post("/login", response_model=Union[TokenLoginResponse, dict])
async def login(
    uow: UOWDep,
    user: UserLoginDTO = Depends(UserLoginDTO.as_form),
    Authorize: AuthJWT = Depends(),
):
    async with uow:
        authenticate = await uow.auth.authenticate_user(
            username=user.username, password=user.password
        )
    if authenticate is False:
        raise HTTPException(status_code=401, detail="Bad username or password")

    access_token = Authorize.create_access_token(subject=user.username)
    refresh_token = Authorize.create_refresh_token(subject=user.username)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post(
    "/refresh",
    response_model=Union[TokenRefreshResponse, Any],
    dependencies=[Depends(JWTBearer())],
)
def refresh(Authorize: AuthJWT = Depends()):
    """
    The jwt_refresh_token_required() function insures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


@router.get(
    "/protected",
    response_model=Union[ProtectedResponse, Any],
    dependencies=[Depends(JWTBearer())],
)
def protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"username": current_user}
