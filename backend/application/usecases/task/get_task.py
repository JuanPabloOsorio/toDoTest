from datetime import datetime
from domain.models.task import Task
from application.ports.outbound.repositories.task_repository import TaskRepository


class GetTaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, task_id: str):
        task: Task = self.task_repository.get_by_id(task_id)
        return task