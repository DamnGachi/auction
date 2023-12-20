from fastapi import APIRouter
from . import health, users, lots, auth

router = APIRouter()


router.include_router(
    health.router,
    prefix="/health",
    tags=["health"],
)

router.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
)
router.include_router(
    lots.router,
    prefix="/lots",
    tags=["lots"],
)
router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
)
