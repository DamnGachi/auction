from pydantic import BaseModel, ConfigDict


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
