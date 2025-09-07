from datetime import datetime
from domain.models.task import Task
from application.ports.outbound.repositories.task_repository import TaskRepository


class GetTasksOfListService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, list_id: str):
        tasks: list[Task] = self.task_repository.get_by_list_id(list_id)
        return tasks