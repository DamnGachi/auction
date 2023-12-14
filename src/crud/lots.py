from datetime import datetime
from uuid import uuid4
from src.dto.lots import LotDTOAdd, LotDTODelete, LotDTOEdit, LotDTOGet, LotDTOArchive
from src.utils.unitofwork import InterfaceUnitOfWork


class LotsService:
    async def move_to_archive(self, uow: InterfaceUnitOfWork, lot: LotDTOArchive):
        lot_dict = lot.model_dump()
        async with uow:
            from src.app.worker.tasks.lots import agent_lots

            lot = await uow.lots.move_archive(id=lot_dict["id"], data=lot_dict)
            await uow.commit()
            # await agent_lots.send(value=lot_dict)
            return lot

    async def add_lot(self, uow: InterfaceUnitOfWork, lot: LotDTOAdd):
        lot_dict = lot.model_dump()
        lot_dict["id"] = uuid4()
        async with uow:
            lot = await uow.lots.add_one(lot_dict)
            await uow.commit()
            return lot_dict

    async def get_lots(self, uow: InterfaceUnitOfWork):
        async with uow:
            lots = await uow.lots.find_all()
            return lots

    async def get_lot(self, uow: InterfaceUnitOfWork, lot: LotDTOGet):
        async with uow:
            reuslt = await uow.lots.find_one(lot)
            return reuslt

    async def edit_lot(self, uow: InterfaceUnitOfWork, lot: LotDTOEdit):
        lot_dict = lot.model_dump()
        id = lot_dict["id"]
        lot_in_db = await self.get_lot(uow, lot)
        if lot_in_db.current_bet > lot.current_bet:
            return False
        async with uow:
            result = await uow.lots.edit_one(id, lot_dict)
            await uow.commit()
            return result

    async def delete_lot(self, uow: InterfaceUnitOfWork, lot: LotDTODelete):
        async with uow:
            lot = await uow.lots.delete_one(lot.id)
            await uow.commit()
            return lot
