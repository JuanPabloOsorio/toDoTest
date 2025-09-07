from typing import Dict, List, Optional
import json
import os
from pathlib import Path
from application.ports.outbound.repositories.task_list_repository import TaskListRepository
from domain.models.list import TaskList
from uuid import uuid4

class JsonTaskListRepository(TaskListRepository):
    """
    JSON file-based implementation of TaskListRepository.
    Stores task lists in a JSON file for persistence across application restarts.
    """
    def __init__(self, file_path=None):
        # Default file path is in the data directory
        if file_path is None:
            # Create data directory if it doesn't exist
            data_dir = Path(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data'))
            data_dir.mkdir(exist_ok=True)
            file_path = data_dir / 'task_lists.json'
        
        self.file_path = file_path
        self.task_lists: Dict[str, TaskList] = {}
        self._load_from_file()
    
    def _load_from_file(self):
        """Load task lists from the JSON file."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                    
                # Convert the JSON data back to TaskList objects
                for task_list_data in data:
                    task_list = TaskList.from_dict(task_list_data)
                    self.task_lists[task_list.id] = task_list
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading task lists from file: {e}")
                # If there's an error, start with an empty dictionary
                self.task_lists = {}
    
    def _save_to_file(self):
        """Save task lists to the JSON file."""
        # Convert TaskList objects to dictionaries
        data = [task_list.to_dict() for task_list in self.task_lists.values()]
        
        # Save to file
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def save(self, task_list: TaskList) -> TaskList:
        """
        Save a task list to the JSON file.
        If the task list has no ID, one will be generated.
        """
        # If task list doesn't have an ID, generate one
        if not hasattr(task_list, 'id') or not task_list.id:
            task_list.id = str(uuid4())

        # Store the task list
        self.task_lists[task_list.id] = task_list
        
        # Save to file
        self._save_to_file()
        
        return task_list

    def update(self, task_list: TaskList) -> TaskList:
        """
        Update a task list in the JSON file.
        If the task list doesn't exist, it will raise an error.
        """
        if not hasattr(task_list, 'id') or not task_list.id:
            raise ValueError("TaskList must have an ID to be updated.")
        
        if task_list.id not in self.task_lists:
            raise ValueError(f"TaskList with ID {task_list.id} does not exist.")
        
        self.task_lists[task_list.id] = task_list
        
        # Save to file
        self._save_to_file()
        
        return task_list

    def get_by_id(self, list_id: str) -> Optional[TaskList]:
        """
        get a task by its ID.
        Returns None if no task is found.
        """
        result = self.task_lists.get(list_id)
        if not result:
            raise ValueError(f"TaskList with ID {list_id} does not exist.")
        return result
    
    def get_all(self) -> List[TaskList]:
        """
        Return all tasks in the repository.
        """
        return list(self.task_lists.values())
    
    def delete(self, id: str) -> None:
        """
        Delete a task list by its ID.
        If the task list doesn't exist, do nothing.
        """
        if id in self.task_lists:
            del self.task_lists[id]
            # Save to file after deletion
            self._save_to_file()