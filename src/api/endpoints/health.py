import importlib
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession

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
    return JSONResponse(status_code=501, content={"error": "NotImplementedError"})


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
