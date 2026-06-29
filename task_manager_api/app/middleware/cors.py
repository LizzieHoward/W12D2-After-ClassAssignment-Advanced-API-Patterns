from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings


def cors_kwargs() -> dict:
    origins = get_settings().cors_origins
    allow_origins = ["*"] if origins == "*" else [item.strip() for item in origins.split(",")]
    return {
        "allow_origins": allow_origins,
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }
