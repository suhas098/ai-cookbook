"""In-memory task store.

Deliberately not a database: this app is a learning surface for DevOps and
Claude Code workflows, not a persistence exercise. State resets on restart -
swapping this module for a real database is a natural next exercise (see
README).
"""

from itertools import count

from app.models import Task, TaskCreate, TaskUpdate

_tasks: dict[int, Task] = {}
_id_seq = count(1)


def list_tasks(done: bool | None = None) -> list[Task]:
    tasks = list(_tasks.values())
    if done is None:
        return tasks
    return [task for task in tasks if task.done == done]


def get_task(task_id: int) -> Task | None:
    return _tasks.get(task_id)


def create_task(payload: TaskCreate) -> Task:
    task = Task(id=next(_id_seq), title=payload.title)
    _tasks[task.id] = task
    return task


def update_task(task_id: int, payload: TaskUpdate) -> Task | None:
    task = _tasks.get(task_id)
    if task is None:
        return None
    updated = task.model_copy(update=payload.model_dump(exclude_unset=True))
    _tasks[task_id] = updated
    return updated


def delete_task(task_id: int) -> bool:
    return _tasks.pop(task_id, None) is not None


def reset() -> None:
    """Test helper: clear all state between test cases."""
    global _id_seq
    _tasks.clear()
    _id_seq = count(1)
