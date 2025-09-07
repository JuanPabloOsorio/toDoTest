from typing import Dict, List, Optional
from application.ports.outbound.repositories.task_list_repository import TaskListRepository
from application.usecases import task
from backend.domain.models.list import TaskList
from uuid import uuid4

class InMemoryTaskListRepository(TaskListRepository):
    """
    In-memory implementation of TaskListRepository for testing and technical
    test purposes.
    """
    
    def __init__(self):
        self.task_lists: Dict[str, TaskList] = {}

    def save(self, task_list: TaskList) -> TaskList:
        """
        Save a task in the in-memory repository.
        If the task has no ID, one will be generated.
        """
        # If task doesn't have an ID, generate one
        if not hasattr(task_list, 'id') or not task_list.id:
            task_list.id = str(uuid4())

        # Store the task
        self.task_lists[task_list.id] = task_list
        return task_list

    def update(self, task_list: TaskList) -> TaskList:
        """
        Update a task in the in-memory repository.
        If the task doesn't exist, it will be created.
        """
        if not hasattr(task_list, 'id') or not task_list.id:
            raise ValueError("TaskList must have an ID to be updated.")
        
        if task_list.id not in self.task_lists:
            raise ValueError(f"TaskList with ID {task_list.id} does not exist.")
        
        self.task_lists[task_list.id] = task_list
        return task_list

    def get_by_id(self, list_id: str) -> Optional[TaskList]:
        """
        get a task by its ID.
        Returns None if no task is found.
        """
        return self.task_lists.get(list_id)
    
    def get_all(self) -> List[TaskList]:
        """
        Return all tasks in the repository.
        """
        return list(self.task_lists.values())
    
    def delete(self, id: str) -> None:
        """
        Delete a task by its ID.
        If the task doesn't exist, do nothing.
        """
        if id in self.task_lists:
            del self.task_lists[id]