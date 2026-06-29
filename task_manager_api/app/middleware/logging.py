import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("task_manager.requests")


class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        started = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - started) * 1000, 2)
        logger.info(
            "request",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "request_id": getattr(request.state, "request_id", ""),
            },
        )
        response.headers["X-Response-Time-ms"] = str(duration_ms)
        return response
