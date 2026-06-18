import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

logger = structlog.get_logger()

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            return await call_next(request)
        except Exception as exc:
            logger.exception("Uncaught exception", path=request.url.path, exception=str(exc))
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": {
                        "code": "INTERNAL_SERVER_ERROR",
                        "message": "Une erreur interne est survenue sur l'ai-service.",
                        "details": str(exc) if request.app.debug else None
                    },
                    "meta": {"model_version_info": "1.0.0"}
                }
            )