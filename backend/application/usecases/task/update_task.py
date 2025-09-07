from datetime import datetime
from domain.models.task import Task
from application.ports.outbound.repositories.task_repository import TaskRepository


class UpdateTaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
    
    def execute(self, task_id: str, updates: dict):
        task: Task = self.task_repository.get_by_id(task_id)
        task.update(**updates)
        self.task_repository.save(task)
        print("task here:", task.to_dict())
        return task