import pytest
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime
from application.usecases.task.update_task import UpdateTaskService
from domain.models.task import Task

class TestUpdateTaskService:
    def setup_method(self):
        """Setup for each test."""
        self.task_repository = Mock()
        self.service = UpdateTaskService(self.task_repository)
        
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
        
        # Create a mock for the updated task
        self.updated_task = Task(
            id=self.task_id,
            title="Updated Task",
            list_id=self.list_id,
            description="Updated Description",
            created_at=self.sample_task.created_at,
            due_date=None,
            attachment=None,
            done=True
        )

    def test_update_task_success(self):
        """Test successful update of a task."""
        # Arrange
        self.task_repository.get_by_id.return_value = self.sample_task
        self.task_repository.save.return_value = self.updated_task
        
        updates = {
            "title": "Updated Task",
            "description": "Updated Description",
            "done": True
        }
        
        # Act
        result = self.service.execute(self.task_id, updates)
        
        # Assert
        self.task_repository.get_by_id.assert_called_once_with(self.task_id)
        self.task_repository.save.assert_called_once()
        assert result.title == "Updated Task"
        assert result.description == "Updated Description"
        assert result.done is True
        
    def test_update_task_not_found(self):
        """Test behavior when task is not found."""
        # Arrange
        self.task_repository.get_by_id.return_value = None
        
        updates = {"title": "Updated Task"}
        self.task_repository.get_by_id.side_effect = Exception("Task not found")
        # Act & Assert
        with pytest.raises(Exception) as excinfo:
            self.service.execute(self.task_id, updates)
        
        assert "Task not found" in str(excinfo.value)
        self.task_repository.get_by_id.assert_called_once_with(self.task_id)
        self.task_repository.save.assert_not_called()
        
    def test_update_task_invalid_data(self):
        """Test behavior when update data is invalid."""
        # Arrange
        self.task_repository.get_by_id.return_value = self.sample_task
        
        # Empty title should raise an exception in Task.update
        updates = {"title": ""}
        
        # Act & Assert
        with pytest.raises(Exception) as excinfo:
            self.service.execute(self.task_id, updates)
            
        assert "Title of the Task could not be empty" in str(excinfo.value)
        self.task_repository.get_by_id.assert_called_once_with(self.task_id)
        self.task_repository.save.assert_not_called()
        
    def test_update_task_repository_error(self):
        """Test behavior when repository raises an exception."""
        # Arrange
        self.task_repository.get_by_id.side_effect = Exception("Database error")
        
        updates = {"title": "Updated Task"}
        
        # Act & Assert
        with pytest.raises(Exception) as excinfo:
            self.service.execute(self.task_id, updates)
            
        assert "Database error" in str(excinfo.value)
        self.task_repository.get_by_id.assert_called_once_with(self.task_id)
        self.task_repository.save.assert_not_called()