from datetime import datetime
from domain.models.task import Task
from application.ports.outbound.repositories.task_repository import TaskRepository


class DeleteTaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, task_id: str):
        return self.task_repository.delete(task_id)