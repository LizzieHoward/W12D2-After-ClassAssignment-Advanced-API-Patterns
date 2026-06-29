import sqlite3
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security import decode_access_token
from app.db.session import get_db
from app.services.user_service import get_user_by_id

security = HTTPBearer(auto_error=False)
DbDep = Annotated[sqlite3.Connection, Depends(get_db)]


def get_current_user(
    db: DbDep,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
) -> dict:
    if credentials is None:
        raise UnauthorizedError("Missing bearer token")
    payload = decode_access_token(credentials.credentials)
    user_id = payload.get("sub")
    if user_id is None:
        raise UnauthorizedError("Invalid token subject")
    return get_user_by_id(db, int(user_id))


def require_admin(current_user: Annotated[dict, Depends(get_current_user)]) -> dict:
    if current_user["role"] != "admin":
        raise ForbiddenError("Admin role required")
    return current_user
