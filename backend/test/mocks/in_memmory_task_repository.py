from typing import Dict, List, Optional
from application.ports.outbound.repositories.task_repository import TaskRepository
from domain.models.task import Task
from uuid import uuid4

class InMemoryTaskRepository(TaskRepository):
    """
    In-memory implementation of TaskRepository for testing and technical
    test purposes.
    """
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
    
    def save(self, task: Task) -> Task:
        """
        Save a task in the in-memory repository.
        If the task has no ID, one will be generated.
        """
        # If task doesn't have an ID, generate one
        if not hasattr(task, 'id') or not task.id:
            task.id = str(uuid4())
            
        # Store the task
        self.tasks[task.id] = task
        return task
    
    def get_by_id(self, id: str) -> Optional[Task]:
        """
        get a task by its ID.
        Returns None if no task is found.
        """
        return self.tasks.get(id)
    
    def get_all(self) -> List[Task]:
        """
        Return all tasks in the repository.
        """
        return list(self.tasks.values())
    
    def delete(self, id: str) -> None:
        """
        Delete a task by its ID.
        If the task doesn't exist, do nothing.
        """
        if id in self.tasks:
            del self.tasks[id]