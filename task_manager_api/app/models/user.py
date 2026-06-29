from dataclasses import dataclass


@dataclass(frozen=True)
class UserModel:
    id: int
    email: str
    full_name: str
    role: str
    created_at: str
