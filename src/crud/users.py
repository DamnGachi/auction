from uuid import uuid4


from src.dto.users import (
    UserDTOAdd,
    UserDTODelete,
    UserDTOEdit,
    UserDTOGet,
)
from src.utils.unitofwork import InterfaceUnitOfWork


class UsersService:
    async def add_user(self, uow: InterfaceUnitOfWork, user: UserDTOAdd):
        user_dict = user.model_dump()
        user_dict["id"] = uuid4()

        async with uow:
            user_id = await uow.users.add_one(user_dict)
            from src.app.worker.tasks.users import agent_users

            await uow.commit()
            await agent_users.send(value=user_dict)
            return user_id

    async def get_users(self, uow: InterfaceUnitOfWork):
        async with uow:
            users = await uow.users.find_all()
            return users

    async def get_user(self, uow: InterfaceUnitOfWork, user: UserDTOGet):
        async with uow:
            user = await uow.users.find_one(user)
            return user

    async def edit_user(self, uow: InterfaceUnitOfWork, user: UserDTOEdit):
        user_dict = user.model_dump()
        for row, value in list(user_dict.items()):
            if value is None:
                del user_dict[f"{row}"]
        id = user_dict["id"]
        async with uow:
            user_id = await uow.users.edit_one(id, user_dict)
            await uow.commit()
            return user_id

    async def delete_user(self, uow: InterfaceUnitOfWork, user_id: UserDTODelete):
        async with uow:
            user = await uow.users.delete_one(user_id.id)
            await uow.commit()
            return user_id
