from uuid import uuid4

from fastapi.responses import JSONResponse

from src.dto.lots import (
    LotDTOAdd,
    LotDTOArchive,
    LotDTOCurrentBet,
    LotDTODelete,
    LotDTOGet,
    LotDTOWinner,
)
from src.utils.unitofwork import InterfaceUnitOfWork


class LotsService:
    async def move_to_archive(self, uow: InterfaceUnitOfWork, lot: LotDTOArchive):
        lot_dict = lot.model_dump()
        async with uow:
            from src.app.worker.tasks.lots import agent_lots

            lot = await uow.lots.move_archive(id=lot_dict["id"], data=lot_dict)
            await uow.commit()
            await agent_lots.send(value=lot_dict)
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
            print(lots)
            return lots

    async def get_lot(self, uow: InterfaceUnitOfWork, lot: LotDTOGet):
        async with uow:
            reuslt = await uow.lots.find_one(lot)
            return reuslt

    async def edit_lot_current_bet(
        self, uow: InterfaceUnitOfWork, lot: LotDTOCurrentBet
    ):
        lot_dict = lot.model_dump()
        data_for_lot = dict()
        data_for_lot["id"] = lot.lot_id
        data_for_lot["current_bet"] = lot.current_bet

        async with uow:
            from src.app.worker.tasks.lots import agent_lots

            not_updated_lot = await uow.lots.find_one(data_for_lot)
            print(not_updated_lot.start_bet)
            if lot.current_bet < not_updated_lot.start_bet:
                return JSONResponse(
                    status_code=409,
                    content={"error": "Bet need to be higher than start bet"},
                )

            update_lot = await uow.lots.edit_one(lot.lot_id, data_for_lot)

            await uow.users.update_user_balance(user_id=lot.user_id, data=lot_dict)
            await uow.commit()
            await agent_lots.send(value=update_lot)
            return update_lot

    async def delete_lot(self, uow: InterfaceUnitOfWork, lot: LotDTODelete):
        async with uow:
            lot = await uow.lots.delete_one(lot.id)
            await uow.commit()
            return lot

    async def lot_winner(self, uow: InterfaceUnitOfWork, lot: LotDTOWinner):
        lot_dict = lot.model_dump()
        async with uow:
            from src.app.worker.tasks.lots import agent_lots

            update_lot = await uow.lots.update_lot_winner(lot_id=lot.id, data=lot_dict)
            await uow.commit()
            await agent_lots.send(value=update_lot)

            return update_lot
