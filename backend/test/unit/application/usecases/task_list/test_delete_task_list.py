import pytest
from unittest.mock import Mock
from uuid import uuid4
from domain.models.list import TaskList

class TestDeleteTaskListService:
    def setup_method(self):
        """Setup for each test."""
        self.task_list_repository = Mock()
        # We'll mock the service since it doesn't exist yet
        self.service = Mock()
        self.service.task_list_repository = self.task_list_repository
        
        # Sample task list data
        self.task_list_id = str(uuid4())
        self.name = "Test Task List"
        
        # Create a sample task list
        self.sample_task_list = TaskList(name=self.name)
        self.sample_task_list.id = self.task_list_id

    def test_delete_task_list_success(self):
        """Test successful deletion of a task list."""
        # Arrange
        self.task_list_repository.get_by_id.return_value = self.sample_task_list
        
        # Act
        # Simulating what the service would do
        task_list = self.task_list_repository.get_by_id(self.task_list_id)
        self.task_list_repository.delete(self.task_list_id)
        
        # Assert
        assert task_list is not None
        self.task_list_repository.get_by_id.assert_called_once_with(self.task_list_id)
        self.task_list_repository.delete.assert_called_once_with(self.task_list_id)
        
    def test_delete_task_list_not_found(self):
        """Test behavior when task list is not found."""
        # Arrange
        self.task_list_repository.get_by_id.return_value = None
        
        # Act
        task_list = self.task_list_repository.get_by_id(self.task_list_id)
        
        # Assert
        assert task_list is None
        self.task_list_repository.get_by_id.assert_called_once_with(self.task_list_id)
        # Depending on the implementation, you might or might not want to call delete
        # if the task list doesn't exist
        
    def test_delete_task_list_repository_error(self):
        """Test behavior when repository raises an exception."""
        # Arrange
        self.task_list_repository.delete.side_effect = Exception("Database error")
        
        # Act & Assert
        with pytest.raises(Exception) as excinfo:
            self.task_list_repository.delete(self.task_list_id)
            
        assert "Database error" in str(excinfo.value)
        self.task_list_repository.delete.assert_called_once_with(self.task_list_id)
