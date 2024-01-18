"""Containers module."""

import asyncio
from dependency_injector import containers, providers
from fastapi import FastAPI
import faust
from src.repositories.users import UsersRepository
from src.repositories.lots import LotsRepository

from src.crud.users import UsersService
from src.crud.lots import LotsService
from src.db.database import async_get_session


class ApplicationContainer(containers.DeclarativeContainer):
    """Application container."""

    config = providers.Configuration(yaml_files=["config.yml"])

    app = FastAPI()
    user_repository = providers.Factory(
        UsersRepository,
        session_factory=async_get_session,
    )

    user_service = providers.Factory(
        UsersService,
        user_repository=user_repository,
    )
    lot_repository = providers.Factory(
        LotsRepository,
        session_factory=async_get_session,
    )

    lot_service = providers.Factory(
        LotsService,
        lot_repository=lot_repository,
    )


class BrokerContainer(containers.DeclarativeContainer):
    faust_app = faust.App(
        "worker",
        broker="kafka://localhost:9092",
        autodiscover=True,
        origin="src.app",
        loop=asyncio.get_running_loop(),
        reply_create_topic=True,
    )
