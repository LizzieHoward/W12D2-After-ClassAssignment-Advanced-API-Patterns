from app.db.init_db import init_db
from app.db.session import get_connection
from app.schemas.task import TaskCreate
from app.schemas.user import UserCreate
from app.services.task_service import create_task, list_tasks
from app.services.user_service import create_user


def test_task_service_filters_by_owner(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'unit.db'}")
    from app.core.config import get_settings

    get_settings.cache_clear()
    db = get_connection()
    init_db(db)
    first_user = create_user(db, UserCreate(email="one@example.com", full_name="One", password="password123"))
    second_user = create_user(db, UserCreate(email="two@example.com", full_name="Two", password="password123"))
    create_task(db, TaskCreate(title="First"), first_user["id"])
    create_task(db, TaskCreate(title="Second"), second_user["id"])

    result = list_tasks(db, first_user, limit=20, offset=0, status=None, sort_by="id", sort_dir="asc")

    assert result["total"] == 1
    assert result["items"][0]["title"] == "First"
    db.close()
