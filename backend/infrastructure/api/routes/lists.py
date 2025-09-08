from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from application.usecases.lists.get_task_list import GetTaskListByIdService
from application.usecases.lists.get_all_lists import GetAllTaskListService
from application.usecases.lists.create_task_list import CreateTaskListService
from application.usecases.lists.update_task_list import UpdateTaskListService
from application.usecases.lists.delete_task_list import DeleteTaskListService
from application.ports.outbound.repositories.task_list_repository import TaskListRepository
from application.ports.outbound.repositories.task_repository import TaskRepository
from application.usecases.lists.get_tasks_of_list import GetTasksOfListService
from dependencies.get_task_list_repo import get_task_list_repository
from dependencies.get_task_repo import get_task_repository


from infrastructure.api.schemas.lists import TaskListBaseSchema, TaskListCreateSchema, TaskListUpdateSchema

router = APIRouter(
    prefix="/lists",
    tags=["task lists"]
)

@router.get("/")
async def get_all_lists(get_task_list_repo: TaskListRepository = Depends(get_task_list_repository)):
    try:
        task_lists = GetAllTaskListService(get_task_list_repo).execute()
        return JSONResponse(
            content={"successful": True, "data": [task.to_dict() for task in task_lists]},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
             content={"successful": False, "error": f"Error listing: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get("/{list_id}")
async def get_list_by_id(list_id: str, get_task_list_repo: TaskListRepository = Depends(get_task_list_repository)):
    try:
        task_list = GetTaskListByIdService(get_task_list_repo).execute(list_id)
        return JSONResponse(
            content={"successful": True, "data": task_list.to_dict()},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
             content={"successful": False, "error": f"Error getting: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get("/{list_id}/tasks")
async def get_tasks_of_list(list_id: str, get_task_repo: TaskRepository = Depends(get_task_repository)):
    try:
        tasks = GetTasksOfListService(get_task_repo).execute(list_id)
        return JSONResponse(
            content={"successful": True, "data": [task.to_dict() for task in tasks]},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
             content={"successful": False, "error": f"Error getting: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.post("/")
async def create_list(new_list: TaskListCreateSchema, get_task_list_repo: TaskListRepository = Depends(get_task_list_repository)):
    try:
        created_task_list = CreateTaskListService(get_task_list_repo).execute(
            name=new_list.name, 
            order=new_list.order
        )
        return JSONResponse(
            content={"successful": True, "data": created_task_list.to_dict()},
            status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        return JSONResponse(
             content={"successful": False, "error": f"Error creating: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.put('/{list_id}')
async def update_list(list_id: str, updates: TaskListUpdateSchema, get_task_list_repo: TaskListRepository = Depends(get_task_list_repository)):
    try:
        updated_task_list = UpdateTaskListService(get_task_list_repo).execute(list_id, updates.model_dump(exclude_none=True))
        return JSONResponse(
            content={"successful": True, "data": updated_task_list.to_dict()},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
            content={"successful": False, "error": f"Error updating: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.delete('/{list_id}')
async def delete_list(list_id: str,
                           get_task_list_repo: TaskListRepository = Depends(get_task_list_repository),
                           get_task_repository: TaskRepository = Depends(get_task_repository)
                           ):
    try:
        DeleteTaskListService(get_task_list_repo, get_task_repository).execute(list_id)
        return JSONResponse(
            content={"successful": True, "message": "Task list deleted successfully"},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
            content={"successful": False, "error": f"Error deleting: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )