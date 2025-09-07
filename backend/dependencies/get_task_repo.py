from application.ports.outbound.repositories.task_repository import TaskRepository
from infrastructure.repositories.json_task_repository import JsonTaskRepository

# Create a single instance to be reused across requests
_task_repo_instance = JsonTaskRepository()

def get_task_repository() -> TaskRepository:
    return _task_repo_instance