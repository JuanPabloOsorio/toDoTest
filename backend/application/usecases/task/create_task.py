from datetime import datetime
from domain.models.task import Task
from application.ports.outbound.repositories.task_repository import TaskRepository
from application.ports.outbound.repositories.task_list_repository import TaskListRepository


class CreateTaskService:
    def __init__(self, task_repository: TaskRepository, task_list_repository: TaskListRepository):
        self.task_repository = task_repository
        self.task_list_repository = task_list_repository
    
    def execute(self,
            title: str,
            list_id: str,
            description: str | None,
            due_date: datetime | None,
            attachment: bytes | bytearray,
            checklist: list = [],
            owner: str = None,
            done: bool = False,
            order: int = 0):

        task_list = self.task_list_repository.get_by_id(list_id)
        if not task_list:
            raise ValueError(f"Task list with ID {list_id} does not exist.")
        task = Task(
            title=title,
            list_id=task_list.id,
            description=description,
            due_date=due_date,
            attachment=attachment,
            checklist=checklist,
            owner=owner,
            done=done,
            order=order
        )

        self.task_repository.save(task)
        return task