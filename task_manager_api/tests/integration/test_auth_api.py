from tests.conftest import register_and_login


def test_register_login_and_me(client):
    token = register_and_login(client)

    response = client.get("/v1/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"
    assert response.headers["X-Request-ID"]
    assert "X-RateLimit-Limit" in response.headers


def test_admin_route_requires_admin_role(client):
    user_token = register_and_login(client, "regular@example.com", "user")
    admin_token = register_and_login(client, "admin@example.com", "admin")

    denied = client.get("/v1/auth/admin", headers={"Authorization": f"Bearer {user_token}"})
    allowed = client.get("/v1/auth/admin", headers={"Authorization": f"Bearer {admin_token}"})

    assert denied.status_code == 403
    assert denied.json()["error"]["code"] == "forbidden"
    assert allowed.status_code == 200
