from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

_FIXED_RESPONSE = {"message": "요청을 처리할 수 없습니다."}


class GlobalExceptionMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        try:
            await self.app(scope, receive, send)
        except Exception as exc:
            request = Request(scope)
            logger.error("%s %s %s: %s", request.method, request.url.path, type(exc).__name__, exc)
            response = JSONResponse(status_code=500, content=_FIXED_RESPONSE)
            await response(scope, receive, send)


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning("%s %s %s %s", request.method, request.url.path, exc.status_code, exc.detail)
    return JSONResponse(status_code=exc.status_code, content=_FIXED_RESPONSE)


def register_exception_handlers(app: FastAPI):
    app.add_middleware(GlobalExceptionMiddleware)
    app.add_exception_handler(HTTPException, http_exception_handler)
