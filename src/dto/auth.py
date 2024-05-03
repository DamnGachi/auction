from fastapi import Form
from pydantic import BaseModel


class ProtectedResponse(BaseModel):
    username: str

    class Config:
        from_attributes = True


class TokenLogin(BaseModel):
    access_token: str
    refresh_token: str


class TokenLoginResponse(TokenLogin):
    class Config:
        from_attributes = True


class TokenRefresh(BaseModel):
    access_token: str


class TokenRefreshResponse(TokenRefresh):
    class Config:
        from_attributes = True


class UserLoginDTO(BaseModel):
    username: str
    password: str

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        password: str = Form(...),
    ):
        return cls(username=username, password=password)
