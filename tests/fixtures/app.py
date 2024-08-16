import pytest

from typing import Generator, AsyncGenerator
from fastapi.testclient import TestClient
from httpx import AsyncClifent
from containers import ApplicationContainer

app = ApplicationContainer.app


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClifent(app=app, base_url=client.base_url) as ac:
        yield ac


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    post_table.clear()
    comment_table.clear()
    yield
