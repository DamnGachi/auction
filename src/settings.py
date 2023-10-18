from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class _AppSettings(_Settings):
    API: str = "api"


class _DatabaseSettings(_Settings):
    DB_USER: str
    DB_NAME: str
    DB_PORT: int
    DB_PASS: str
    DB_HOST: str

    @property
    def DB_URI(self):
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=f"/{self.DB_NAME}",
        )


app_settings = _AppSettings()
db_settings = _DatabaseSettings()
