from src.dto.users import UserDtoAdd
from src.utils.unitofwork import InterfaceUnitOfWork


class UsersService:
    async def add_user(self, uow: InterfaceUnitOfWork, user: UserDtoAdd):
        user_dict = user.model_dump()
        async with uow:
            user_id = await uow.users.add_one(user_dict)
            await uow.commit()
            return user_id

    async def get_users(self, uow: InterfaceUnitOfWork):
        async with uow:
            users = await uow.users.find_all()
            return users
