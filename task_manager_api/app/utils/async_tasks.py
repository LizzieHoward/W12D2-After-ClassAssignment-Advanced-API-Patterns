from datetime import datetime, timezone
from pathlib import Path


def record_task_event(message: str) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    with Path("background_events.log").open("a", encoding="utf-8") as handle:
        handle.write(f"{timestamp} {message}\n")
