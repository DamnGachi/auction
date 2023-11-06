from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy import exc

from src.dto.lots import LotDtoAdd
from .dependencies import UOWDep
from src.dto.users import UserDtoAdd, UserDtoDelete, UserDtoEdit, UserDtoGet
from src.crud.users import UsersService


router = APIRouter()


@router.put("/")
async def move_lot_to_archive():
    pass


@router.put("/")
async def create_lot():
    pass


@router.get("/")
async def get_lots():
    pass

@router.delete("/")
async def delete_lot():
    pass