from typing import Any, List, Union

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, paginate
from sqlalchemy import exc
from sqlalchemy.exc import NoResultFound

from src.crud.lots import LotsService
from src.dto.lots import (
    LotDTOAdd,
    LotDTOCurrentBet,
    LotDTODelete,
    LotDTOGet,
    LotDTOGets,
    LotDTORead,
    LotDTOWinner,
)

from .dependencies import UOWDep

router = APIRouter()


# @router.put("/", response_model=Union[LotDTOArchive, Any])
# async def move_lot_to_archive(
#     uow: UOWDep,
#     lot: LotDTOArchive = Depends(LotDTOArchive.as_form),
# ):
#     try:
#         lot_archived = await LotsService().move_to_archive(uow, lot)
#         if lot_archived is None:
#             raise NoResultFound
#         return lot_archived
#     except NoResultFound:
#         # Ошибка, если лот не найден
#         return JSONResponse(status_code=404, content={"error": "Lot not found"})


@router.patch("/")
async def lot_winner(
    uow: UOWDep,
    lot: LotDTOWinner = Depends(LotDTOWinner.as_form),
):
    """Закрывает лот и изменяет сумму пользователя"""
    try:
        lot_archived = await LotsService().lot_winner(uow, lot)
        if lot_archived is None:
            raise NoResultFound
        return lot_archived
    except NoResultFound:
        # Ошибка, если лот не найден
        return JSONResponse(status_code=404, content={"error": "Lot not found"})


# @router.patch("/current_bet")
# async def lot_current_bet(
#     uow: UOWDep,
#     lot: LotDTOCurrentBet = Depends(LotDTOCurrentBet.as_form),
# ):
#     """Изменяет текущию ставку лота"""
#     lot = await LotsService().lot_current_bet(uow, lot)


@router.post("/", response_model=Union[LotDTOAdd, Any])
async def create_lot(
    uow: UOWDep,
    lot: LotDTOAdd = Depends(LotDTOAdd.as_form),
):
    created_lot = await LotsService().add_lot(uow, lot)
    return created_lot


@router.post("/one", response_model=Union[LotDTORead, Any])
async def get_lot(uow: UOWDep, lot: LotDTOGet = Depends(LotDTOGet.as_form)):
    try:
        result = await LotsService().get_lot(uow, lot)
        return result
    except exc.NoResultFound:
        return JSONResponse(status_code=404, content={"error": "Lot Not Found"})


@router.get("/all", response_model=Page[Union[List[LotDTOGets], Any]])
async def get_lots(
    uow: UOWDep,
):
    lots = await LotsService().get_lots(uow)
    # return lots

    return paginate(lots)


@router.delete("/")
async def delete_lot(uow: UOWDep, lot: LotDTODelete = Depends(LotDTODelete.as_form)):
    lot_id = await LotsService().delete_lot(uow, lot)
    if lot_id is not None:
        return {"message": "Lot was deleted"}
    return JSONResponse(status_code=404, content={"error": "Lot Not Found"})


@router.patch("/current_bet", response_model=Union[LotDTOCurrentBet, Any])
async def lot_current_bet(
    uow: UOWDep, lot: LotDTOCurrentBet = Depends(LotDTOCurrentBet.as_form)
):
    """Изменяет ставку лота"""
    try:
        result = await LotsService().edit_lot_current_bet(uow, lot)
        return result
    except exc.NoResultFound:
        return JSONResponse(status_code=404, content={"error": "Lot Not Found"})
    except ValueError:
        # Ошибка, если лот закрылся с ставкой превушающий баланс пользователя
        return JSONResponse(
            status_code=403,
            content={"error": "Your bet is too high for your balance"},
        )
