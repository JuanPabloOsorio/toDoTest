
from abc import ABC, abstractmethod


# application/ports/task_repository.py
from abc import ABC, abstractmethod
from domain.models.list import TaskList

class TaskListRepository(ABC):
    @abstractmethod
    def save(self, task_list: TaskList) -> TaskList: ...
    
    @abstractmethod
    def get_by_id(self, list_id: str) -> TaskList | None: ...

    @abstractmethod
    def get_all(self) -> list[TaskList]: ...
    
    @abstractmethod
    def delete(self, list_id: str) -> None: ...
    
    @abstractmethod
    def update(self, task_list: TaskList) -> TaskList: ...