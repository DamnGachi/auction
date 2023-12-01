from typing import Any, Union, List
from fastapi import APIRouter, Depends

from sqlalchemy import exc
from fastapi_pagination import Page, add_pagination, paginate
from .dependencies import UOWDep
from src.dto.lots import (
    LotDTOAdd,
    LotDTODelete,
    LotDTOEdit,
    LotDTOGets,
    LotDTOGet,
    LotDTORead,
)
from src.crud.lots import LotsService


router = APIRouter()


@router.put("/")
async def move_lot_to_archive(
    uow: UOWDep,
):
    pass


@router.post("/", response_model=Union[LotDTOAdd, Any])
async def create_lot(
    uow: UOWDep,
    lot: LotDTOAdd = Depends(LotDTOAdd.as_form),
):
    created_lot = await LotsService().add_lot(uow, lot)
    return created_lot


@router.post("/one", response_model=Union[LotDTORead, Any])
async def get_lot(uow: UOWDep, lot: LotDTOGet = Depends(LotDTOGet.as_form)):
    result = await LotsService().get_lot(uow, lot)
    return result


@router.get("/all", response_model=Page[Union[List[LotDTOGets], Any]])
async def get_lots(
    uow: UOWDep,
):
    lots = await LotsService().get_lots(uow)
    return paginate(lots)


@router.delete("/")
async def delete_lot():
    pass


@router.patch("/", response_model=Union[LotDTOEdit, Any])
async def edit_lot(uow: UOWDep, lot: LotDTOEdit = Depends(LotDTOEdit.as_form)):
    """Изменяет ставку лота когда её перебивает другой аукционер"""
    result = await LotsService().edit_lot(uow, lot)
    return result
