from uuid import UUID
from sqlalchemy import update
from src.models.main import Lot
from src.utils.repository import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession


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

        res = await self.session.execute(stmt)
        return res.scalar_one()
