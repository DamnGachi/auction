
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException


def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    """
    :type request: Request
    :param request:
    :param exc:
    :return:
    """
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


async def not_found(request: Request, exc: Exception) -> Response:
    return Response(b"404 Not Found")

async def internal_server_error(request: Request, exc: Exception) -> Response:
    return Response(b"500 Not Found")