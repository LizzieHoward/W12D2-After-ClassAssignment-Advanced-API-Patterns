from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

TaskStatus = Literal["todo", "in_progress", "done"]


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    description: str | None = Field(default=None, max_length=1000)
    status: TaskStatus = "todo"
    priority: int = Field(default=3, ge=1, le=5)


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=160)
    description: str | None = Field(default=None, max_length=1000)
    status: TaskStatus | None = None
    priority: int | None = Field(default=None, ge=1, le=5)


class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: int
    owner_id: int
    created_at: datetime | str
    updated_at: datetime | str


class TaskList(BaseModel):
    items: list[TaskRead]
    total: int
    limit: int
    offset: int
