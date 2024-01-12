"""Containers module."""

import asyncio
from dependency_injector import containers, providers
from fastapi import FastAPI
import faust


class ApplicationContainer(containers.DeclarativeContainer):
    """Application container."""

    config = providers.Configuration(yaml_files=["config.yml"])

    app = FastAPI()


class BrokerContainer(containers.DeclarativeContainer):
    faust_app = faust.App(
        "worker",
        broker="kafka://localhost:9092",
        autodiscover=True,
        origin="src.app",
        loop=asyncio.get_running_loop(),
        reply_create_topic=True,
    )
