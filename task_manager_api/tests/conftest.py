import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret-key-with-at-least-32-bytes")
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6399/0")
    monkeypatch.setenv("RATE_LIMIT_REQUESTS", "100")
    monkeypatch.setenv("RATE_LIMIT_WINDOW_SECONDS", "60")

    from app.core.config import get_settings
    from app.core.rate_limit import reset_rate_limit_fallback
    from app.utils.caching import cache_clear

    get_settings.cache_clear()
    reset_rate_limit_fallback()
    cache_clear()

    from app.main import app

    with TestClient(app) as test_client:
        yield test_client

    if Path("background_events.log").exists():
        Path("background_events.log").unlink()


def register_and_login(client: TestClient, email: str = "user@example.com", role: str = "user") -> str:
    payload = {
        "email": email,
        "full_name": "Test User",
        "password": "password123",
        "role": role,
    }
    response = client.post("/v1/auth/register", json=payload)
    assert response.status_code == 201
    login = client.post("/v1/auth/login", json={"email": email, "password": "password123"})
    assert login.status_code == 200
    return login.json()["access_token"]
