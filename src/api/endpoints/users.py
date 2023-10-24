from fastapi import APIRouter

from .dependencies import UOWDep
from src.dto.users import UserDtoAdd
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
