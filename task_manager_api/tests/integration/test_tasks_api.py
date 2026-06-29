from tests.conftest import register_and_login


def test_task_crud_filter_sort_pagination_and_cache(client):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    first = client.post("/v1/tasks", json={"title": "Write API", "priority": 2}, headers=headers)
    second = client.post(
        "/v1/tasks",
        json={"title": "Review docs", "status": "done", "priority": 5},
        headers=headers,
    )

    assert first.status_code == 201
    assert second.status_code == 201

    listing = client.get("/v1/tasks?status=done&sort_by=priority&sort_dir=desc&limit=1&offset=0", headers=headers)
    assert listing.status_code == 200
    body = listing.json()
    assert body["total"] == 1
    assert body["items"][0]["title"] == "Review docs"

    task_id = first.json()["id"]
    updated = client.patch(f"/v1/tasks/{task_id}", json={"status": "in_progress"}, headers=headers)
    assert updated.status_code == 200
    assert updated.json()["status"] == "in_progress"

    stats_miss = client.get("/v1/tasks/stats", headers=headers)
    stats_hit = client.get("/v1/tasks/stats", headers=headers)
    assert stats_miss.headers["X-Cache"] == "MISS"
    assert stats_hit.headers["X-Cache"] == "HIT"
    assert stats_hit.json()["total"] == 2

    deleted = client.delete(f"/v1/tasks/{task_id}", headers=headers)
    assert deleted.status_code == 204


def test_users_cannot_read_other_users_tasks_but_admin_can(client):
    user_token = register_and_login(client, "owner@example.com", "user")
    other_token = register_and_login(client, "other@example.com", "user")
    admin_token = register_and_login(client, "admin2@example.com", "admin")
    task = client.post("/v1/tasks", json={"title": "Private task"}, headers={"Authorization": f"Bearer {user_token}"})
    task_id = task.json()["id"]

    denied = client.get(f"/v1/tasks/{task_id}", headers={"Authorization": f"Bearer {other_token}"})
    allowed = client.get(f"/v1/tasks/{task_id}", headers={"Authorization": f"Bearer {admin_token}"})

    assert denied.status_code == 403
    assert allowed.status_code == 200
