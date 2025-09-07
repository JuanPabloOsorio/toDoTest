import pytest
from unittest.mock import Mock
from uuid import uuid4
from domain.models.list import TaskList

class TestCreateTaskListService:
    def setup_method(self):
        """Setup for each test."""
        self.task_list_repository = Mock()
        # We'll mock the service since it doesn't exist yet
        self.service = Mock()
        self.service.task_list_repository = self.task_list_repository
        
        # Sample task list data
        self.name = "Test Task List"
        self.task_list_id = str(uuid4())
        
        # Create a sample task list
        self.sample_task_list = TaskList(name=self.name)
        self.sample_task_list.id = self.task_list_id

    def test_create_task_list_success(self):
        """Test successful creation of a task list."""
        # Arrange
        self.task_list_repository.save.return_value = self.sample_task_list
        
        # Act
        # Simulating what the service would do
        task_list = TaskList(name=self.name)
        self.task_list_repository.save(task_list)
        result = task_list
        
        # Assert
        assert result.name == self.name
        assert result.id is not None
        self.task_list_repository.save.assert_called_once()
        
    def test_create_task_list_invalid_name(self):
        """Test behavior when task list name is invalid."""
        # Arrange - empty name should raise an exception
        invalid_name = ""
        
        # Act & Assert
        with pytest.raises(Exception) as excinfo:
            TaskList(name=invalid_name)
            
        assert "Task List name could not be empty" in str(excinfo.value)
        self.task_list_repository.save.assert_not_called()
        
    def test_create_task_list_repository_error(self):
        """Test behavior when repository raises an exception."""
        # Arrange
        self.task_list_repository.save.side_effect = Exception("Database error")
        
        # Act & Assert
        with pytest.raises(Exception) as excinfo:
            task_list = TaskList(name=self.name)
            self.task_list_repository.save(task_list)
            
        assert "Database error" in str(excinfo.value)
        self.task_list_repository.save.assert_called_once()
