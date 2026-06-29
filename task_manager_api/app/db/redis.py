from typing import Any

from app.core.config import get_settings


async def get_redis_client() -> Any | None:
    try:
        from redis.asyncio import Redis

        client = Redis.from_url(
            get_settings().redis_url,
            decode_responses=True,
            socket_connect_timeout=0.1,
            socket_timeout=0.1,
        )
        await client.ping()
        return client
    except Exception:
        return None
