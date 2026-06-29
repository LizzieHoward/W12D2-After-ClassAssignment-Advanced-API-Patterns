import sqlite3

from app.core.exceptions import ConflictError, NotFoundError
from app.core.security import hash_password
from app.schemas.user import UserCreate


def row_to_user(row: sqlite3.Row) -> dict:
    return dict(row)


def create_user(db: sqlite3.Connection, payload: UserCreate) -> dict:
    try:
        cursor = db.execute(
            "INSERT INTO users (email, full_name, hashed_password, role) VALUES (?, ?, ?, ?)",
            (payload.email.lower(), payload.full_name, hash_password(payload.password), payload.role),
        )
        db.commit()
    except sqlite3.IntegrityError as exc:
        raise ConflictError("A user with that email already exists") from exc
    return get_user_by_id(db, cursor.lastrowid)


def get_user_by_email(db: sqlite3.Connection, email: str) -> dict | None:
    row = db.execute("SELECT * FROM users WHERE email = ?", (email.lower(),)).fetchone()
    return row_to_user(row) if row else None


def get_user_by_id(db: sqlite3.Connection, user_id: int) -> dict:
    row = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if row is None:
        raise NotFoundError("User not found")
    return row_to_user(row)
