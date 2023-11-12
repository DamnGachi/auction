from datetime import datetime
from uuid import uuid4
from src.dto.lots import LotDtoAdd, LotDtoDelete, LotDtoEdit, LotDtoGet
from src.utils.unitofwork import InterfaceUnitOfWork


class LotsService:
    async def add_lot(self, uow: InterfaceUnitOfWork, lot: LotDtoAdd):
        lot_dict = lot.model_dump()
        lot_dict["id"] = uuid4()
        async with uow:
            lot_id = await uow.lots.add_one(lot_dict)
            await uow.commit()
            return lot_id

    async def get_lots(self, uow: InterfaceUnitOfWork):
        async with uow:
            lots = await uow.lots.find_all()
            return lots

    async def get_lot(self, uow: InterfaceUnitOfWork, lot: LotDtoGet):
        lot_dict = lot.model_dump()
        async with uow:
            lot_id = await uow.lots.find_one(lot_dict)
            return lot_id

    async def edit_lot(self, uow: InterfaceUnitOfWork, lot: LotDtoEdit):
        lot_dict = lot.model_dump()
        id = lot_dict["id"]
        async with uow:
            lot_id = await uow.lots.edit_one(id, lot_dict)
            await uow.commit()
            return lot_id

    async def delete_lot(self, uow: InterfaceUnitOfWork, lot_id: LotDtoDelete):
        async with uow:
            lot = await uow.lots.delete_one(lot_id)
            await uow.commit()
            return lot
