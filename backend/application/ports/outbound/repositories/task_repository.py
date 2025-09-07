from abc import ABC, abstractmethod


# application/ports/task_repository.py
from abc import ABC, abstractmethod
from domain.models.task import Task

class TaskRepository(ABC):
    @abstractmethod
    def save(self, task: Task) -> Task: ...
    
    @abstractmethod
    def get_by_id(self, id: str) -> Task | None: ...
    
    @abstractmethod
    def get_all(self) -> list[Task]: ...
    
    @abstractmethod
    def delete(self, id: str) -> None: ...

    @abstractmethod
    def get_by_list_id(self, list_id: str) -> list[Task]: ...