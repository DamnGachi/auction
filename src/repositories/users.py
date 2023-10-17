from models.main import User
from utils.repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = User