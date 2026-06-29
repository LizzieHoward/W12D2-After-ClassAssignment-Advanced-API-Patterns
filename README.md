# W12D2 Advanced API Patterns: Production-Ready API System

This repository contains a compact FastAPI task manager API built for the W12D2 Advanced API Patterns assignment. It focuses on the required production-style patterns without adding paid services or unnecessary framework complexity.

## What is included

- Versioned FastAPI routes under `/v1`
- User registration with bcrypt password hashing
- Login with JWT bearer access tokens
- Protected user route and admin-only RBAC route
- Task CRUD resource with pagination, status filtering, and sorting
- Pydantic request/response validation
- CORS configuration
- Redis-backed rate limiting with `X-RateLimit-*` headers and a documented in-memory fallback
- Async `httpx` external API endpoint at `/v1/external/uuid`
- `BackgroundTasks` example on task creation
- In-memory response caching example at `/v1/tasks/stats`
- Request ID middleware using `X-Request-ID`
- Structured request logging
- Standardized error responses and global exception handlers
- `/v1/health` and `/v1/health/detailed`
- Pytest unit and integration tests
- Dockerfile and Docker Compose with API and Redis
- Optional Postman collection

## Project layout

```text
task_manager_api/
  app/
    api/v1/        # auth, task, health, external routes
    core/          # config, security, errors, rate limiting, logging
    db/            # sqlite connection and schema initialization
    middleware/    # request id, structured logging, CORS helper
    schemas/       # Pydantic models
    services/      # explicit business/data logic
    utils/         # cache and background task helpers
  tests/
  Dockerfile
  docker-compose.yml
  .env.example
```

## Local setup

From the repository root:

```bash
cd task_manager_api
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and replace `JWT_SECRET_KEY` with a local development value. Do not commit real secrets.

Run the API:

```bash
uvicorn app.main:app --reload
```

Open:

- API docs: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/v1/health`
- Detailed health: `http://127.0.0.1:8000/v1/health/detailed`

## Docker Compose

Docker Compose starts the API plus Redis:

```bash
cd task_manager_api
docker compose up --build
```

The API will be available at `http://127.0.0.1:8000`.

## Environment variables

| Variable | Purpose | Default/example |
| --- | --- | --- |
| `DATABASE_URL` | SQLite database URL | `sqlite:///./task_manager.db` |
| `JWT_SECRET_KEY` | JWT signing key | replace locally |
| `ACCESS_TOKEN_MINUTES` | Token lifetime | `60` |
| `CORS_ORIGINS` | Comma-separated origins or `*` | `*` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `RATE_LIMIT_REQUESTS` | Requests per window | `100` |
| `RATE_LIMIT_WINDOW_SECONDS` | Rate limit window | `60` |
| `CACHE_TTL_SECONDS` | In-memory cache TTL | `30` |

## API examples

Register:

```bash
curl -X POST http://127.0.0.1:8000/v1/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"user@example.com\",\"full_name\":\"User Example\",\"password\":\"password123\",\"role\":\"user\"}"
```

Login:

```bash
curl -X POST http://127.0.0.1:8000/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"user@example.com\",\"password\":\"password123\"}"
```

Create a task:

```bash
curl -X POST http://127.0.0.1:8000/v1/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Finish assignment\",\"priority\":2}"
```

List tasks with query options:

```bash
curl "http://127.0.0.1:8000/v1/tasks?status=todo&limit=20&offset=0&sort_by=priority&sort_dir=asc" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Testing

```bash
cd task_manager_api
python -m pytest
python -m pytest --cov
```

The tests use temporary SQLite databases and do not require Redis. If Redis is unavailable, the app logs rate-limit state in an in-memory fallback so the local API remains reviewable. Docker Compose is the preferred path for testing Redis-backed behavior.

## Known limitations

- SQLite is used for coursework simplicity. A production system would usually use Postgres or another managed database.
- The cache example is in-memory. It demonstrates the strategy and headers, but it is not shared across multiple API instances.
- The async external endpoint calls `https://httpbin.org/uuid`, so it requires internet access at runtime.
- No live deployment or demo video is included in this overdue triage pass.
