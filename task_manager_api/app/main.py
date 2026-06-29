from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError

from app.api.v1 import auth, external, health, tasks
from app.core.config import get_settings
from app.core.exceptions import AppError
from app.core.logging import configure_logging
from app.core.rate_limit import RateLimitMiddleware
from app.db.init_db import init_db
from app.db.session import get_connection
from app.middleware.cors import CORSMiddleware, cors_kwargs
from app.middleware.logging import StructuredLoggingMiddleware
from app.middleware.request_id import RequestIDMiddleware
from app.utils.responses import error_response

configure_logging()
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = get_connection()
    init_db(conn)
    conn.close()
    yield


app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, **cors_kwargs())
app.add_middleware(StructuredLoggingMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(RequestIDMiddleware)


@app.exception_handler(AppError)
def app_error_handler(request: Request, exc: AppError):
    return error_response(request, exc.status_code, exc.error_code, exc.message)


@app.exception_handler(RequestValidationError)
def validation_error_handler(request: Request, exc: RequestValidationError):
    return error_response(
        request,
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "validation_error",
        "Request validation failed",
        exc.errors(),
    )


@app.exception_handler(Exception)
def unhandled_error_handler(request: Request, exc: Exception):
    return error_response(request, status.HTTP_500_INTERNAL_SERVER_ERROR, "internal_error", "Unexpected server error")


app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(tasks.router, prefix=settings.api_prefix)
app.include_router(health.router, prefix=settings.api_prefix)
app.include_router(external.router, prefix=settings.api_prefix)


@app.get("/")
def root() -> dict:
    return {"message": "Task Manager API", "docs": "/docs", "version": settings.api_prefix}
