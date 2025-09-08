from domain.models.list import TaskList
from application.ports.outbound.repositories.task_list_repository import TaskListRepository


class UpdateTaskListService:
    def __init__(self, task_list_repository: TaskListRepository):
        self.task_list_repository = task_list_repository
    
    def execute(self, list_id: str, updates: dict):
        task_list: TaskList = self.task_list_repository.get_by_id(list_id)
        task_list.update(**updates)
        self.task_list_repository.save(task_list)
        return task_list