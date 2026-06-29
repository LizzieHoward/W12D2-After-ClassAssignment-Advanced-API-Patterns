import sqlite3

from app.core.exceptions import UnauthorizedError
from app.core.security import create_access_token, verify_password
from app.schemas.auth import LoginRequest
from app.services.user_service import get_user_by_email


def authenticate_user(db: sqlite3.Connection, payload: LoginRequest) -> tuple[str, dict]:
    user = get_user_by_email(db, payload.email)
    if user is None or not verify_password(payload.password, user["hashed_password"]):
        raise UnauthorizedError("Incorrect email or password")
    token = create_access_token(str(user["id"]), user["role"])
    return token, user
