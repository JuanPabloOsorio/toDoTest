from typing import Dict, List, Optional
import json
import os
from datetime import datetime
from pathlib import Path
from application.ports.outbound.repositories.task_repository import TaskRepository
from domain.models.task import Task
from uuid import uuid4

class JsonTaskRepository(TaskRepository):
    """
    JSON file-based implementation of TaskRepository.
    Stores tasks in a JSON file for persistence across application restarts.
    """
    def __init__(self, file_path=None):
        # Default file path is in the data directory
        if file_path is None:
            # Create data directory if it doesn't exist
            data_dir = Path(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data'))
            data_dir.mkdir(exist_ok=True)
            file_path = data_dir / 'task.json'
        
        self.file_path = file_path
        self.tasks: Dict[str, Task] = {}
        self._load_from_file()
    
    def _load_from_file(self):
        """Load tasks from the JSON file."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                    
                # Convert the JSON data back to Task objects
                for task_data in data:
                    task = Task.from_dict(task_data)
                    self.tasks[task.id] = task
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading tasks from file: {e}")
                # If there's an error, start with an empty dictionary
                self.tasks = {}
    
    def _save_to_file(self):
        """Save tasks to the JSON file."""
        # Convert Task objects to dictionaries
        data = [task.to_dict() for task in self.tasks.values()]
        
        # Save to file
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def save(self, task: Task) -> Task:
        """
        Save a task to the JSON file.
        If the task has no ID, one will be generated.
        """
        # If task doesn't have an ID, generate one
        if not hasattr(task, 'id') or not task.id:
            task.id = str(uuid4())
            
        # Store the task
        self.tasks[task.id] = task
        
        # Save to file
        self._save_to_file()
        
        return task
    
    def get_by_id(self, id: str) -> Optional[Task]:
        """
        Get a task by its ID.
        Returns None if no task is found.
        """
        result = self.tasks.get(id)
        if not result:
            raise ValueError(f"Task with ID {id} does not exist.")
        return result
    
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
            # Save to file after deletion
            self._save_to_file()
    
    def get_by_list_id(self, list_id: str) -> List[Task]:
        """
        Get all tasks that belong to a specific list.
        """
        return [task for task in self.tasks.values() if task.list_id == list_id]
