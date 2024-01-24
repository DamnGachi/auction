import importlib
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import kafka
from sqlalchemy import select

# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.worker.tasks.health import health_check

from src.app.logger import logger
from src.db.database import async_get_session

router = APIRouter()


@router.get(
    "/broker",
    responses={
        200: {
            "description": "Broker avaliable",
            "content": {"application/json": {"example": {"successful": True}}},
        },
        500: {
            "description": "Broker not avaliable",
            "content": {"application/json": {"example": {"successful": False}}},
        },
    },
)
async def health() -> JSONResponse:
    """Send message to broker, for helath check"""
    try:
        data = {"health": True}
        await health_check.send(value=data)
        return JSONResponse(status_code=200, content={"successful": True})
    except kafka.errors.KafkaConnectionError:
        return JSONResponse(status_code=500, content={"successful": False})


@router.get(
    "/api",
    responses={
        200: {
            "description": "API avaliable",
            "content": {"application/json": {"example": {"successful": True}}},
        },
    },
)
async def health() -> JSONResponse:
    return JSONResponse(status_code=200, content={"successful": True})


@router.get(
    "/db",
    responses={
        200: {
            "description": "Database avaliable",
            "content": {"application/json": {"example": {"successful": True}}},
        },
        500: {
            "description": "Database not avaliable",
            "content": {"application/json": {"example": {"successful": False}}},
        },
    },
)
async def health(session: AsyncSession = Depends(async_get_session)) -> JSONResponse:
    try:
        async with session as cursor:
            await cursor.scalar(select(1))
        return JSONResponse(status_code=200, content={"successful": True})
    except Exception as error:
        logger.exception(error)
        return JSONResponse(status_code=500, content={"successful": False})
