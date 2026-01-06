# W12D2-After-ClassAssignment-Advanced-API-Patterns
## Project Structure
task_manager_api/
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── tasks.py
│   │       └── health.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── rate_limit.py
│   │   └── logging.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── task.py
│   │   └── common.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   └── task_service.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── session.py
│   │   ├── init_db.py
│   │   └── redis.py
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── request_id.py
│   │   ├── logging.py
│   │   └── cors.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── caching.py
│       ├── responses.py
│       └── async_tasks.py
│
├── tests/
│   ├── unit/
│   │   ├── test_auth_service.py
│   │   └── test_task_service.py
│   │
│   ├── integration/
│   │   ├── test_auth_api.py
│   │   ├── test_tasks_api.py
│   │   └── test_rate_limiting.py
│   │
│   └── conftest.py
│
├── docker/
│   └── redis.conf
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── README.md
├── requirements.txt
└── pyproject.toml
