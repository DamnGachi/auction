from sqlalchemy import select
from src.models.main import User
from src.utils.repository import SQLAlchemyRepository
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthRepository(SQLAlchemyRepository):
    model = User

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    async def authenticate_user(self, username: str, password: str):
        stmt = select(User).where(User.username == username)
        rows = await self.session.execute(stmt)
        user = rows.scalar_one_or_none()
        if user and self.verify_password(password, user.password):
            return user
        else:
            return False
