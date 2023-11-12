from fastapi import APIRouter, Depends

from sqlalchemy import exc

from .dependencies import UOWDep
from src.dto.lots import LotDtoAdd, LotDtoDelete, LotDtoEdit, LotDtoGet
from src.crud.lots import LotsService


router = APIRouter()


@router.put("/")
async def move_lot_to_archive(
    uow: UOWDep,
):
    pass


@router.post("/")
async def create_lot(
    uow: UOWDep,
    lot: LotDtoAdd = Depends(LotDtoAdd.as_form),
):
    lot_id = await LotsService().add_lot(uow, lot)
    return {"lot_id": lot_id}


@router.get("/")
async def get_lots():
    pass


@router.delete("/")
async def delete_lot():
    pass
