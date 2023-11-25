from typing import Any, Union,List
from fastapi import APIRouter, Depends

from sqlalchemy import exc
from fastapi_pagination import Page, add_pagination, paginate
from .dependencies import UOWDep
from src.dto.lots import LotDtoAdd, LotDtoDelete, LotDtoEdit, LotDtoGet
from src.crud.lots import LotsService


router = APIRouter()


@router.put("/")
async def move_lot_to_archive(
    uow: UOWDep,
):
    pass


@router.post("/", response_model=Union[LotDtoAdd, Any])
async def create_lot(
    uow: UOWDep,
    lot: LotDtoAdd = Depends(LotDtoAdd.as_form),
):
    created_lot = await LotsService().add_lot(uow, lot)
    return created_lot


@router.get("/", response_model=Page[Union[List[LotDtoGet], Any]])
async def get_lots(
    uow: UOWDep,
):
    lots = await LotsService().get_lots(uow)
    return paginate(lots)


@router.delete("/")
async def delete_lot():
    pass
