import asyncio
import importlib
import sys
from pathlib import Path

from fastapi.responses import HTMLResponse, RedirectResponse
from src.app.logger import logger

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))

from fastapi import FastAPI, HTTPException, Request, Response, status
from src.api import api_router
from src.app.consumer.init import get_faust_app, set_faust_app_for_api
from src.utils.exception_handlers import internal_server_error, not_found

app = FastAPI(debug=True)


def create_app() -> FastAPI:
    app = FastAPI()

    @app.post("/increment", response_class=RedirectResponse)
    async def increment():
        increment_task = importlib.import_module(
            "app.worker.tasks.increment",
        )
        await increment_task.agent.ask()

        # redirect the user back to the entrypoint
        return RedirectResponse(
            url=app.url_path_for("entrypoint"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    @app.get("/", response_class=HTMLResponse)
    async def entrypoint():
        get_current_count_task = importlib.import_module(
            "app.worker.tasks.get_current_count",
        )
        count = await get_current_count_task.agent.ask()

        return f"""
            <h1>Current count: {count}</h1>
            <form method="post" action="/increment">
                <input type="submit" value="Increment!">
            </form>
            """

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

    app.include_router(api_router, prefix="/api")  # prefix=app_settings.API
    app.add_exception_handler(HTTPException, not_found)
    app.add_exception_handler(HTTPException, internal_server_error)
    return app
