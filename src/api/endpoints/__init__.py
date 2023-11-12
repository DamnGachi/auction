from fastapi import APIRouter
from . import health, users, lots

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
