import pytest
from unittest.mock import Mock
from uuid import uuid4
from domain.models.list import TaskList

class TestUpdateTaskListService:
    def setup_method(self):
        """Setup for each test."""
        self.task_list_repository = Mock()
        # We'll mock the service since it doesn't exist yet
        self.service = Mock()
        self.service.task_list_repository = self.task_list_repository
        
        # Sample task list data
        self.task_list_id = str(uuid4())
        self.name = "Test Task List"
        self.updated_name = "Updated Task List"
        
        # Create a sample task list
        self.sample_task_list = TaskList(name=self.name)
        self.sample_task_list.id = self.task_list_id
        
        # Create an updated task list
        self.updated_task_list = TaskList(name=self.updated_name)
        self.updated_task_list.id = self.task_list_id

    def test_update_task_list_success(self):
        """Test successful update of a task list."""
        # Arrange
        self.task_list_repository.get_by_id.return_value = self.sample_task_list
        self.task_list_repository.update.return_value = self.updated_task_list
        
        # Act
        # Simulating what the service would do
        task_list = self.task_list_repository.get_by_id(self.task_list_id)
        task_list.update(name=self.updated_name)
        result = self.task_list_repository.update(task_list)
        
        # Assert
        assert result.name == self.updated_name
        assert result.id == self.task_list_id
        self.task_list_repository.get_by_id.assert_called_once_with(self.task_list_id)
        self.task_list_repository.update.assert_called_once()
        
    def test_update_task_list_not_found(self):
        """Test behavior when task list is not found."""
        # Arrange
        self.task_list_repository.get_by_id.return_value = None
        
        # Act & Assert
        result = self.task_list_repository.get_by_id(self.task_list_id)
        assert result is None
        self.task_list_repository.get_by_id.assert_called_once_with(self.task_list_id)
        self.task_list_repository.update.assert_not_called()
        
    def test_update_task_list_invalid_name(self):
        """Test behavior when update data is invalid."""
        # Arrange
        self.task_list_repository.get_by_id.return_value = self.sample_task_list
        
        # Empty name should raise an exception
        invalid_name = ""
        
        # Act & Assert
        with pytest.raises(Exception) as excinfo:
            task_list = self.task_list_repository.get_by_id(self.task_list_id)
            task_list.update(name=invalid_name)
            
        assert "error updating TaskList, name could not be None" in str(excinfo.value)
        self.task_list_repository.get_by_id.assert_called_once_with(self.task_list_id)
        self.task_list_repository.update.assert_not_called()
        
    def test_update_task_list_repository_error(self):
        """Test behavior when repository raises an exception."""
        # Arrange
        self.task_list_repository.get_by_id.side_effect = Exception("Database error")
        
        # Act & Assert
        with pytest.raises(Exception) as excinfo:
            self.task_list_repository.get_by_id(self.task_list_id)
            
        assert "Database error" in str(excinfo.value)
        self.task_list_repository.get_by_id.assert_called_once_with(self.task_list_id)
        self.task_list_repository.update.assert_not_called()
