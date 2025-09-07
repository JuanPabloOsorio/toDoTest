from application.ports.outbound.repositories.task_repository import TaskRepository
from application.ports.outbound.repositories.task_list_repository import TaskListRepository


class DeleteTaskListService:
    def __init__(self, task_list_repository: TaskListRepository, task_repository: TaskRepository):
        self.task_repository = task_repository
        self.task_list_repository = task_list_repository

    def execute(self, list_id: str):
        tasks = self.task_repository.get_by_list_id(list_id)
        for task in tasks:
            self.task_repository.delete(task.id)
        return self.task_list_repository.delete(list_id)