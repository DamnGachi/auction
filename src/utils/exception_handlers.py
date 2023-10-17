
from fastapi import Request, Response


async def not_found(request: Request, exc: Exception) -> Response:
    return Response(b"404 Not Found")

async def internal_server_error(request: Request, exc: Exception) -> Response:
    return Response(b"500 Not Found")