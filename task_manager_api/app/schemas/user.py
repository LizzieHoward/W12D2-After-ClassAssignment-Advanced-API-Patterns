from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field

Role = Literal["user", "admin"]


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=120)
    password: str = Field(min_length=8, max_length=128)
    role: Role = "user"


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: Role
    created_at: datetime | str
