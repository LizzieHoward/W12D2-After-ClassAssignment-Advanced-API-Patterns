from app.core.config import get_settings
from app.core.rate_limit import reset_rate_limit_fallback


def test_rate_limit_returns_headers_and_429(client, monkeypatch):
    monkeypatch.setenv("RATE_LIMIT_REQUESTS", "2")
    get_settings.cache_clear()
    reset_rate_limit_fallback()

    first = client.get("/")
    second = client.get("/")
    third = client.get("/")

    assert first.status_code == 200
    assert second.status_code == 200
    assert third.status_code == 429
    assert third.headers["X-RateLimit-Limit"] == "2"
    assert third.json()["error"]["code"] == "rate_limited"
