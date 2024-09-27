from fastapi import FastAPI
import pytest

from typing import Generator, AsyncGenerator
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from containers import ApplicationContainer

# /from src.app.main import create_app
# container = ApplicationContainer()
app = ApplicationContainer.app
# app = create_app()

# app.container = container


@pytest.mark.anyio
async def test_async_client():
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://127.0.0.1:8500/api/v1/"
    ) as ac:
        response = await ac.get("users/all")
        assert response.status_code == 404
    print(response)


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture
def anyio_backend():
    return "asyncio"


# @pytest.fixture(autouse=True)
# async def db() -> AsyncGenerator:
#     post_table.clear()
#     comment_table.clear()
#     yield
