import time
from typing import Any

from app.core.config import get_settings

_cache: dict[str, tuple[float, Any]] = {}


def cache_get(key: str) -> Any | None:
    item = _cache.get(key)
    if item is None:
        return None
    expires_at, value = item
    if expires_at < time.time():
        _cache.pop(key, None)
        return None
    return value


def cache_set(key: str, value: Any) -> None:
    _cache[key] = (time.time() + get_settings().cache_ttl_seconds, value)


def cache_clear() -> None:
    _cache.clear()
