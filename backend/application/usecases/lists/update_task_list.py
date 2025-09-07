from domain.models.list import TaskList
from application.ports.outbound.repositories.task_repository import TaskRepository


class UpdateTaskListService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
    
    def execute(self, list_id: str, updates: dict):
        task: TaskList = self.task_repository.get_by_id(list_id)
        task.update(**updates)
        self.task_repository.save(task)
        return task