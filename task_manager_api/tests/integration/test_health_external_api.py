import httpx


def test_health_endpoints(client):
    assert client.get("/v1/health").json() == {"status": "ok"}
    detailed = client.get("/v1/health/detailed")
    assert detailed.status_code == 200
    assert detailed.json()["checks"]["database"] == "ok"


def test_external_uuid_endpoint_uses_async_httpx(client, monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"uuid": "00000000-0000-0000-0000-000000000000"}

    class FakeAsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return None

        async def get(self, url):
            assert url == "https://httpbin.org/uuid"
            return FakeResponse()

    monkeypatch.setattr(httpx, "AsyncClient", FakeAsyncClient)

    response = client.get("/v1/external/uuid")

    assert response.status_code == 200
    assert response.json()["uuid"] == "00000000-0000-0000-0000-000000000000"
