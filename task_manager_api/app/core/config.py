from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Task Manager API"
    environment: str = "development"
    api_prefix: str = "/v1"
    database_url: str = "sqlite:///./task_manager.db"
    jwt_secret_key: str = "dev-only-secret-replace-in-env-32-bytes"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60
    cors_origins: str = "*"
    redis_url: str = "redis://redis:6379/0"
    rate_limit_requests: int = 100
    rate_limit_window_seconds: int = 60
    cache_ttl_seconds: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
