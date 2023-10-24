import sqlalchemy as sa
from sqlalchemy import MetaData
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from src.dto.users import UserDtoRead


@as_declarative()
class Base(object):
    __name__: str
    metadata: MetaData

    @classmethod
    @declared_attr
    def __tablename__(cls):  # noqa: N805
        return cls.__name__.lower()

    # @classmethod
    # def to_read_model(cls):
    #     return UserDtoRead(
    #         id=cls.id,
    #         username=cls.username,
    #         hashed_password=cls.hashed_password,
    #         balance=cls.balance,
    #     )
