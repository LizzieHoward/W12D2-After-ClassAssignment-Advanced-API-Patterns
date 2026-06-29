import sqlite3

from app.core.exceptions import ForbiddenError, NotFoundError
from app.schemas.task import TaskCreate, TaskUpdate

ALLOWED_SORT_FIELDS = {"id", "created_at", "updated_at", "priority", "status", "title"}


def _row_to_task(row: sqlite3.Row) -> dict:
    return dict(row)


def create_task(db: sqlite3.Connection, payload: TaskCreate, owner_id: int) -> dict:
    cursor = db.execute(
        """
        INSERT INTO tasks (title, description, status, priority, owner_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (payload.title, payload.description, payload.status, payload.priority, owner_id),
    )
    db.commit()
    return get_task(db, cursor.lastrowid, {"id": owner_id, "role": "admin"})


def list_tasks(
    db: sqlite3.Connection,
    current_user: dict,
    limit: int,
    offset: int,
    status: str | None,
    sort_by: str,
    sort_dir: str,
) -> dict:
    sort_by = sort_by if sort_by in ALLOWED_SORT_FIELDS else "created_at"
    direction = "DESC" if sort_dir.lower() == "desc" else "ASC"
    clauses: list[str] = []
    params: list[object] = []
    if current_user["role"] != "admin":
        clauses.append("owner_id = ?")
        params.append(current_user["id"])
    if status:
        clauses.append("status = ?")
        params.append(status)
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    total = db.execute(f"SELECT COUNT(*) AS count FROM tasks {where}", params).fetchone()["count"]
    rows = db.execute(
        f"SELECT * FROM tasks {where} ORDER BY {sort_by} {direction} LIMIT ? OFFSET ?",
        (*params, limit, offset),
    ).fetchall()
    return {"items": [_row_to_task(row) for row in rows], "total": total, "limit": limit, "offset": offset}


def get_task(db: sqlite3.Connection, task_id: int, current_user: dict) -> dict:
    row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        raise NotFoundError("Task not found")
    task = _row_to_task(row)
    if current_user["role"] != "admin" and task["owner_id"] != current_user["id"]:
        raise ForbiddenError("You do not have access to this task")
    return task


def update_task(db: sqlite3.Connection, task_id: int, payload: TaskUpdate, current_user: dict) -> dict:
    existing = get_task(db, task_id, current_user)
    data = payload.model_dump(exclude_unset=True)
    if not data:
        return existing
    fields = ", ".join(f"{key} = ?" for key in data)
    values = [*data.values(), task_id]
    db.execute(f"UPDATE tasks SET {fields}, updated_at = CURRENT_TIMESTAMP WHERE id = ?", values)
    db.commit()
    return get_task(db, task_id, current_user)


def delete_task(db: sqlite3.Connection, task_id: int, current_user: dict) -> None:
    get_task(db, task_id, current_user)
    db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
