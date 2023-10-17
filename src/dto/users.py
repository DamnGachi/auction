from pydantic import BaseModel


class UserDtoAdd(BaseModel):
    username: str
