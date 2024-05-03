from uuid import UUID
from sqlalchemy import update
from src.models.main import User
from src.utils.repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = User

    async def update_user_balance(self, user_id: UUID, data: dict) -> int:
        new_data = dict()
        balance = (await self.find_one(filter_by={"id": user_id})).balance
        if balance < data["current_bet"]:
            raise ValueError
        new_balance = balance - data["current_bet"]
        new_data["balance"] = new_balance
        stmt = (
            update(self.model)
            .values(**new_data)
            .filter_by(id=user_id)
            .returning(self.model.id, self.model.balance)
        )

        rows = await self.session.execute(stmt)
        res = rows.fetchone()
        return {
            "user_id": res.id,
            "user_balance": res.balance,
        }
