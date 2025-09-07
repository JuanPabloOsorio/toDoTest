from application.ports.outbound.repositories.task_list_repository import TaskListRepository
from infrastructure.repositories.json_task_list_repository import JsonTaskListRepository

# Create a single instance to be reused across requests
_task_list_repo_instance = JsonTaskListRepository()

def get_task_list_repository() -> TaskListRepository:
    return _task_list_repo_instance