
from fastapi import FastAPI, Request, Response


app = FastAPI(debug=True)


@app.route("/error")
async def error(request: Request) -> Response:
    raise RuntimeError("Oh no")


@app.exception_handler(404)
async def not_found(request: Request, exc: Exception) -> Response:
    return Response(b"404 Not Found")

@app.exception_handler(500)
async def internal_server_error(request: Request, exc: Exception) -> Response:
    return Response(b"500 Not Found")