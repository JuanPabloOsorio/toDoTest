from domain.models.list import TaskList
from application.ports.outbound.repositories.task_list_repository import TaskListRepository


class CreateTaskListService:
    def __init__(self, task_list_repository: TaskListRepository):
        self.task_list_repository = task_list_repository

    def execute(self, name: str):
        task = TaskList(name=name)
        self.task_list_repository.save(task)
        return task