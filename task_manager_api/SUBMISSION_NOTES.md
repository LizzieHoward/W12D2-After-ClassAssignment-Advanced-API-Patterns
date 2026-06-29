# Submission Notes

## Implemented

- FastAPI application with versioned `/v1` routes.
- Auth flow with registration, bcrypt password hashing, JWT login, `/auth/me`, and admin-only RBAC route.
- Task CRUD API with pagination, filtering, sorting, and owner/admin access rules.
- Request validation with Pydantic schemas.
- CORS setup.
- Redis-first rate limiting with `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, and `429` responses. If Redis is unavailable, the app uses an in-memory fallback for local review.
- Standardized error responses with global exception handlers.
- Request ID middleware using `X-Request-ID`.
- Structured request logging.
- Health endpoints at `/v1/health` and `/v1/health/detailed`.
- Background task example writes task creation events to `background_events.log`.
- Async external API example at `/v1/external/uuid` using `httpx.AsyncClient`.
- In-memory response caching example at `/v1/tasks/stats` with `X-Cache` headers.
- Unit and integration tests.
- Dockerfile and Docker Compose with API and Redis.
- Postman collection.

## Commands to run

```bash
cd task_manager_api
python -m pip install -r requirements.txt
python -m pytest
python -m pytest --cov
docker compose config
```

## Known limitations

- SQLite is used to keep the assignment locally reviewable.
- Response caching is in-memory rather than Redis-backed.
- The external API endpoint requires internet access.
- Live deployment and demo video were not completed as part of this repo-focused triage pass.
