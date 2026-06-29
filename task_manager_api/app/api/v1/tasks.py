from fastapi import APIRouter, BackgroundTasks, Depends, Query, Response, status

from app.api.deps import DbDep, get_current_user
from app.schemas.task import TaskCreate, TaskList, TaskRead, TaskUpdate
from app.services import task_service
from app.utils.async_tasks import record_task_event
from app.utils.caching import cache_get, cache_set

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    background_tasks: BackgroundTasks,
    db: DbDep,
    current_user: dict = Depends(get_current_user),
) -> dict:
    task = task_service.create_task(db, payload, current_user["id"])
    background_tasks.add_task(record_task_event, f"created task {task['id']} for user {current_user['id']}")
    return task


@router.get("", response_model=TaskList)
def list_tasks(
    db: DbDep,
    current_user: dict = Depends(get_current_user),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    status_filter: str | None = Query(default=None, alias="status"),
    sort_by: str = Query(default="created_at"),
    sort_dir: str = Query(default="desc", pattern="^(asc|desc)$"),
) -> dict:
    return task_service.list_tasks(db, current_user, limit, offset, status_filter, sort_by, sort_dir)


@router.get("/stats", response_model=dict)
def task_stats(response: Response, db: DbDep, current_user: dict = Depends(get_current_user)) -> dict:
    cache_key = f"task_stats:{current_user['id']}:{current_user['role']}"
    cached = cache_get(cache_key)
    if cached is not None:
        response.headers["X-Cache"] = "HIT"
        return cached
    tasks = task_service.list_tasks(db, current_user, limit=100, offset=0, status=None, sort_by="id", sort_dir="asc")
    stats = {"total": tasks["total"], "by_status": {"todo": 0, "in_progress": 0, "done": 0}}
    for task in tasks["items"]:
        stats["by_status"][task["status"]] += 1
    cache_set(cache_key, stats)
    response.headers["X-Cache"] = "MISS"
    return stats


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: DbDep, current_user: dict = Depends(get_current_user)) -> dict:
    return task_service.get_task(db, task_id, current_user)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate, db: DbDep, current_user: dict = Depends(get_current_user)) -> dict:
    return task_service.update_task(db, task_id, payload, current_user)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: DbDep, current_user: dict = Depends(get_current_user)) -> Response:
    task_service.delete_task(db, task_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
