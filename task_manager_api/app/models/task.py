from dataclasses import dataclass


@dataclass(frozen=True)
class TaskModel:
    id: int
    title: str
    description: str | None
    status: str
    priority: int
    owner_id: int
    created_at: str
    updated_at: str
