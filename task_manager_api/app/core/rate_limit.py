import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.config import get_settings
from app.db.redis import get_redis_client

_fallback_counts: dict[str, tuple[int, float]] = {}


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        settings = get_settings()
        if request.url.path in {"/health", "/v1/health", "/v1/health/detailed"}:
            return await call_next(request)

        limit = settings.rate_limit_requests
        window = settings.rate_limit_window_seconds
        identity = request.client.host if request.client else "unknown"
        key = f"rate:{identity}:{int(time.time() // window)}"
        count = await self._increment(key, window)
        remaining = max(limit - count, 0)
        reset = int((int(time.time() // window) + 1) * window)
        headers = {
            "X-RateLimit-Limit": str(limit),
            "X-RateLimit-Remaining": str(remaining),
            "X-RateLimit-Reset": str(reset),
        }
        if count > limit:
            request_id = getattr(request.state, "request_id", "")
            return JSONResponse(
                status_code=429,
                content={
                    "error": {
                        "code": "rate_limited",
                        "message": "Too many requests",
                        "status_code": 429,
                    },
                    "request_id": request_id,
                },
                headers=headers,
            )
        response = await call_next(request)
        response.headers.update(headers)
        return response

    async def _increment(self, key: str, window: int) -> int:
        client = await get_redis_client()
        if client is not None:
            count = await client.incr(key)
            if count == 1:
                await client.expire(key, window)
            await client.aclose()
            return int(count)
        count, expires_at = _fallback_counts.get(key, (0, time.time() + window))
        if expires_at < time.time():
            count, expires_at = 0, time.time() + window
        count += 1
        _fallback_counts[key] = (count, expires_at)
        return count


def reset_rate_limit_fallback() -> None:
    _fallback_counts.clear()
