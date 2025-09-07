from domain.models.list import TaskList
from application.ports.outbound.repositories.task_list_repository import TaskListRepository


class GetAllTaskListService:
    def __init__(self, task_list_repository: TaskListRepository):
        self.task_list_repository = task_list_repository

    def execute(self):
        task_lists: list[TaskList] = self.task_list_repository.get_all()
        return task_lists