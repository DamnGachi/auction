from src.models.main import Lot, User
from src.utils.repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = User


class LotsRepository(SQLAlchemyRepository):
    model = Lot
