from fastapi import APIRouter, Depends, status

from app.api.deps import DbDep, get_current_user, require_admin
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserRead
from app.services.auth_service import authenticate_user
from app.services.user_service import create_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: DbDep) -> dict:
    return create_user(db, payload)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: DbDep) -> dict:
    token, user = authenticate_user(db, payload)
    return {"access_token": token, "token_type": "bearer", "user": user}


@router.get("/me", response_model=UserRead)
def read_me(current_user: dict = Depends(get_current_user)) -> dict:
    return current_user


@router.get("/admin", response_model=dict)
def admin_only(current_user: dict = Depends(require_admin)) -> dict:
    return {"message": "Admin access granted", "user_id": current_user["id"]}
