import pytest
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime
from application.usecases.lists.get_tasks_of_list import GetTasksOfListService
from domain.models.task import Task

class TestGetTasksByListIdService:
    def setup_method(self):
        """Setup for each test."""
        self.task_repository = Mock()
        self.service = GetTasksOfListService(self.task_repository)
        
        # Sample list ID
        self.list_id = str(uuid4())
        
        # Sample tasks data
        self.task1 = Task(
            id=str(uuid4()),
            title="Task 1",
            list_id=self.list_id,
            description="Description 1",
            created_at=datetime.now(),
            due_date=None,
            attachment=None,
            done=False
        )
        
        self.task2 = Task(
            id=str(uuid4()),
            title="Task 2",
            list_id=self.list_id,
            description="Description 2",
            created_at=datetime.now(),
            due_date=None,
            attachment=None,
            done=True
        )
        
        self.sample_tasks = [self.task1, self.task2]

    def test_get_tasks_by_list_id_success(self):
        """Test successful retrieval of tasks by list ID."""
        # Arrange
        self.task_repository.get_by_list_id.return_value = self.sample_tasks
        
        # Act
        result = self.service.execute(self.list_id)
        
        # Assert
        assert result == self.sample_tasks
        assert len(result) == 2
        self.task_repository.get_by_list_id.assert_called_once_with(self.list_id)

    def test_get_tasks_by_list_id_empty(self):
        """Test behavior when no tasks are found for a list ID."""
        # Arrange
        self.task_repository.get_by_list_id.return_value = []
        
        # Act
        result = self.service.execute(self.list_id)
        
        # Assert
        assert result == []
        assert len(result) == 0
        self.task_repository.get_by_list_id.assert_called_once_with(self.list_id)

    def test_get_tasks_by_list_id_repository_error(self):
        """Test behavior when repository raises an exception."""
        # Arrange
        self.task_repository.get_by_list_id.side_effect = Exception("Error retrieving tasks")
        
        # Act & Assert
        with pytest.raises(Exception) as excinfo:
            self.service.execute(self.list_id)
        
        assert "Error retrieving tasks" in str(excinfo.value)
        self.task_repository.get_by_list_id.assert_called_once_with(self.list_id)