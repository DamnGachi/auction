from uuid import UUID

from src.dto.users import UserDtoAdd, UserDtoDelete, UserDtoEdit, UserDtoGet
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

    async def get_user(self, uow: InterfaceUnitOfWork, user: UserDtoGet):
        user_dict = user.model_dump()
        async with uow:
            user_id = await uow.users.find_one(user_dict)
            return user_id

    async def edit_user(self, uow: InterfaceUnitOfWork, user: UserDtoEdit):
        user_dict = user.model_dump()
        id = user_dict["id"]
        async with uow:
            user_id = await uow.users.edit_one(id, user_dict)
            await uow.commit()
            return user_id

    async def delete_user(self, uow: InterfaceUnitOfWork, user_id: UserDtoDelete):
        async with uow:
            user_id = await uow.users.edit_one(user_id)
            await uow.commit()
            return user_id
