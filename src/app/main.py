import asyncio
import sys
from pathlib import Path

from fastapi_pagination import add_pagination
from pydantic import BaseModel

from src.app.logger import logger

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from src.api import api_router
from src.app.worker.init import get_faust_app, set_faust_app_for_api
from src.utils.exception_handlers import (
    authjwt_exception_handler,
    internal_server_error,
    not_found,
)

app = FastAPI(debug=True)


def create_app() -> FastAPI:
    app = FastAPI()

    class Settings(BaseModel):
        authjwt_secret_key: str = "secret"

    @AuthJWT.load_config
    def get_config():
        """
        :return:
        """
        return Settings()

    @app.on_event("startup")
    async def startup_event():
        logger.info("Initializing API ...")
        # set up the faust app
        set_faust_app_for_api()

        faust_app = get_faust_app()

        # start the faust app in client mode
        asyncio.create_task(faust_app.start_client())

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down API")
        faust_app = get_faust_app()
        # graceful shutdown
        await faust_app.stop()

    add_pagination(app)
    app.include_router(api_router, prefix="/api")  # prefix=app_settings.API
    app.add_exception_handler(HTTPException, not_found)
    app.add_exception_handler(HTTPException, internal_server_error)
    app.add_exception_handler(AuthJWTException, authjwt_exception_handler)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # not for production
        allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
        allow_headers=[
            "Content-Type",
            "Set-Cookie",
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Origin",
            "Authorization",
        ],
        allow_credentials=True,
    )
    return app
