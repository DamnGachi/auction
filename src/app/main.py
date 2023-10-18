import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))

from fastapi import FastAPI, HTTPException, Request, Response
from src.api import api_router

# from src.settings import app_settings
from src.utils.exception_handlers import internal_server_error, not_found

app = FastAPI(debug=True)


def create_app() -> FastAPI:
    app = FastAPI()

    @app.route("/error")
    async def error(request: Request) -> Response:
        raise RuntimeError("Oh no")

    @app.route("/health_db")
    async def health(request: Request) -> Response:
        raise RuntimeError("Oh no")

    app.include_router(api_router, prefix="/api")  # prefix=app_settings.API
    app.add_exception_handler(HTTPException, not_found)
    app.add_exception_handler(HTTPException, internal_server_error)
    return app
