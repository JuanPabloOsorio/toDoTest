import pytest
from unittest.mock import Mock, patch
from uuid import uuid4
from datetime import datetime
from application.usecases.task.get_task import GetTaskService
from domain.models.task import Task

# Import the service to test (using absolute import)

class TestGetTaskService:
    def setup_method(self):
        """Setup for each test."""
        self.task_repository = Mock()
        self.service = GetTaskService(self.task_repository)
        
        # Sample task data
        self.task_id = str(uuid4())
        self.list_id = str(uuid4())
        self.sample_task = Task(
            id=self.task_id,
            title="Test Task",
            list_id=self.list_id,
            description="Test Description",
            created_at=datetime.now(),
            due_date=None,
            attachment=None,
            done=False
        )

    def test_get_task_success(self):
        """Test successful retrieval of a task."""
        # Arrange
        self.task_repository.get_by_id.return_value = self.sample_task
        
        # Act
        result = self.service.execute(self.task_id)
        
        # Assert
        assert result == self.sample_task
        self.task_repository.get_by_id.assert_called_once_with(self.task_id)

    def test_get_task_not_found(self):
        """Test behavior when task is not found."""
        # Arrange
        self.task_repository.get_by_id.side_effect = Exception("Task not found")
        
        # Act & Assert
        with pytest.raises(Exception) as excinfo:
            self.service.execute(self.task_id)
        
        assert "Task not found" in str(excinfo.value)
        self.task_repository.get_by_id.assert_called_once_with(self.task_id)


    def test_get_task_repository_error(self):
        """Test behavior when repository raises an exception."""
        # Arrange
        self.task_repository.get_by_id.side_effect = Exception("Error retrieving task")
        
        # Act & Assert
        with pytest.raises(Exception) as excinfo:
            self.service.execute(self.task_id)
        
        assert "Error retrieving task" in str(excinfo.value)
        self.task_repository.get_by_id.assert_called_once_with(self.task_id)
