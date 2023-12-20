from typing import Any, Union
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from src.db.database import async_get_session
from src.app.basic import Hasher, JWTBearer
from src.dto.users import UserDTOAdd, UserDTORead
from src.dto.auth import TokenLoginResponse, TokenRefreshResponse, ProtectedResponse

router = APIRouter()


@router.post(
    "/register",
    response_model=Union[UserDTORead, Any],
    dependencies=[Depends(JWTBearer())],
)
async def register(
    user: UserDTOAdd = Depends(UserDTOAdd.as_form),
    Authorize: AuthJWT = Depends(),
    session: Session = Depends(async_get_session),
) -> dict:
    pass
    # Authorize.jwt_required()
    # username = Authorize.get_jwt_subject()
    # user_admin = await UserDAL._is_admin(username, session)
    # if user_admin is False:
    #     raise HTTPException(status_code=403, detail="You are not administrator")
    # user = await UserDAL._create_admin_user(user, session)
    # if not user:
    #     return {"Username already registered"}
    # return user


@router.post("/login", response_model=Union[TokenLoginResponse, Any])
async def login(
    user: UserDTOAdd = Depends(UserDTOAdd.as_form),
    Authorize: AuthJWT = Depends(),
    session: Session = Depends(async_get_session),
):
    authenticate = await Hasher().authenticate_user(
        username=user.username, password=user.password, session=session
    )
    if authenticate == False:
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
