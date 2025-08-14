from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from dependency import get_request_user_id, get_tasks_service
from exceptions import TaskNotFound, CategoryNotFound
from schemas.tasks import TaskSchema, TaskCreateSchema, TaskUpdateSchema
from services.tasks import TasksService

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post(
    path="/",
    response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    body: TaskCreateSchema,
    task_service: Annotated[TasksService, Depends(get_tasks_service)],
    user_id: int = Depends(get_request_user_id)
):
    return task_service.create_task(body, user_id)


@router.get("/all", response_model=list[TaskSchema])
def get_all_tasks(
        task_service: Annotated[TasksService, Depends(get_tasks_service)],
):
    return task_service.get_all_tasks()



@router.get("/{task_id}")
def get_task(
        task_id: int,
        task_service: Annotated[TasksService, Depends(get_tasks_service)],
):
    return task_service.get_task_by_id(task_id)

@router.patch("/{task_id}", response_model=TaskSchema)
def patch_task(
    task_id: int,
    body: TaskUpdateSchema,
    task_service: Annotated[TasksService, Depends(get_tasks_service)],
    user_id: int = Depends(get_request_user_id),
):
    try:
        return task_service.update_task_name(task_id=task_id, body=body.name, user_id=user_id)
    except CategoryNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@router.delete("/{task_id}")
def delete_task(
        task_id: int,
        task_service: Annotated[TasksService, Depends(get_tasks_service)],
        user_id: int = Depends(get_request_user_id),
):
    try:
        task_service.delete_task(task_id=task_id, user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
