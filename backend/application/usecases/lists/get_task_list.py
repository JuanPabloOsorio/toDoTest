from domain.models.list import TaskList
from application.ports.outbound.repositories.task_list_repository import TaskListRepository


class GetTaskListByIdService:
    def __init__(self, task_repository: TaskListRepository):
        self.task_repository = task_repository

    def execute(self, list_id: str):
        task_list: TaskList = self.task_repository.get_by_id(list_id)
        return task_list