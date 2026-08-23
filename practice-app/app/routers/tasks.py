from fastapi import APIRouter, HTTPException

from app import store
from app.models import Task, TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[Task])
def list_tasks(done: bool | None = None) -> list[Task]:
    return store.list_tasks(done=done)


@router.post("", response_model=Task, status_code=201)
def create_task(payload: TaskCreate) -> Task:
    return store.create_task(payload)


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    task = store.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskUpdate) -> Task:
    task = store.update_task(task_id, payload)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int) -> None:
    if not store.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
