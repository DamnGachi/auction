from uuid import UUID

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.main import Lot
from src.utils.repository import SQLAlchemyRepository


class LotsRepository(SQLAlchemyRepository):
    model = Lot

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def move_archive(self, id: UUID, data: dict) -> int:
        stmt = (
            update(self.model)
            .values(**data)
            .filter_by(id=id)
            .returning(
                self.model.id,
                self.model.title,
                self.model.description,
                self.model.is_active,
                self.model.current_bet,
                self.model.closed_at,
                self.model.closed_bet,
            )
        )

        rows = await self.session.execute(stmt)
        res = rows.fetchone()
        return res

    async def lot_winner(self, id: UUID, data: dict) -> int:
        stmt = (
            update(self.model)
            .values(**data)
            .filter_by(id=id)
            .returning(
                self.model.id,
                self.model.winner_uid,
                self.model.closed_bet,
                self.model.closed_at,
            )
        )

        rows = await self.session.execute(stmt)
        res = rows.fetchone()
        return res
