from fastapi import APIRouter

from app.core.config import get_settings
from app.db.redis import get_redis_client
from app.db.session import get_connection

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health() -> dict:
    return {"status": "ok"}


@router.get("/detailed")
async def detailed_health() -> dict:
    database = "ok"
    redis = "unavailable"
    try:
        conn = get_connection()
        conn.execute("SELECT 1")
        conn.close()
    except Exception:
        database = "error"
    client = await get_redis_client()
    if client is not None:
        redis = "ok"
        await client.aclose()
    return {
        "status": "ok" if database == "ok" else "degraded",
        "environment": get_settings().environment,
        "checks": {"database": database, "redis": redis},
    }
