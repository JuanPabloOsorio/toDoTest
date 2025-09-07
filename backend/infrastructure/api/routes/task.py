from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from application.usecases.task.get_task import GetTaskService
from application.usecases.lists.get_tasks_of_list import GetTasksOfListService
from application.usecases.task.create_task import CreateTaskService
from application.usecases.task.update_task import UpdateTaskService
from application.usecases.task.delete_task import DeleteTaskService
from application.ports.outbound.repositories.task_repository import TaskRepository
from application.ports.outbound.repositories.task_list_repository import TaskListRepository
from dependencies.get_task_repo import get_task_repository
from dependencies.get_task_list_repo import get_task_list_repository

from infrastructure.api.schemas.task import TaskCreateSchema, TaskUpdateSchema, TaskBaseSchema

router = APIRouter(
    prefix="/task",
    tags=["tasks"]
)


@router.get("/{task_id}")
async def get_task(task_id: str, get_task_repo: TaskRepository = Depends(get_task_repository)):
    try:
        task = GetTaskService(get_task_repo).execute(task_id)
        return JSONResponse(
            content={"successful": True, "data": task.to_dict()},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
             content={"successful": False, "error": f"Error getting: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



@router.post("/")
async def create_task(task: TaskCreateSchema,
                    get_task_repo: TaskRepository = Depends(get_task_repository),
                    get_task_list_repo: TaskListRepository = Depends(get_task_list_repository)
                    ):
    try:
        created_task = CreateTaskService(get_task_repo, get_task_list_repo).execute(**task.model_dump())
        return JSONResponse(
            content={"successful": True, "data": created_task.to_dict()},
            status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        return JSONResponse(
             content={"successful": False, "error": f"Error creating: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.put('/{task_id}')
async def update_task(task_id: str, updates: TaskUpdateSchema, get_task_repo: TaskRepository = Depends(get_task_repository)):
    try:
        updated_task = UpdateTaskService(get_task_repo).execute(task_id, updates.model_dump(exclude_none=True))
        return JSONResponse(
            content={"successful": True, "data": updated_task.to_dict()},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
            content={"successful": False, "error": f"Error updating: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.delete('/{task_id}')
async def delete_task(task_id: str, get_task_repo: TaskRepository = Depends(get_task_repository)):
    try:
        DeleteTaskService(get_task_repo).execute(task_id)
        return JSONResponse(
            content={"successful": True, "message": "Task deleted successfully"},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
            content={"successful": False, "error": f"Error deleting: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )