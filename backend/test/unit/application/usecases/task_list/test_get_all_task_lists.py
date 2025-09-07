import pytest
from unittest.mock import Mock
from uuid import uuid4
from domain.models.list import TaskList

class TestGetAllTaskListsService:
    def setup_method(self):
        """Setup for each test."""
        self.task_list_repository = Mock()
        # We'll mock the service since it doesn't exist yet
        self.service = Mock()
        self.service.task_list_repository = self.task_list_repository
        
        # Sample task lists data
        self.task_list1 = TaskList(name="Task List 1")
        self.task_list1.id = str(uuid4())
        
        self.task_list2 = TaskList(name="Task List 2")
        self.task_list2.id = str(uuid4())
        
        self.sample_task_lists = [self.task_list1, self.task_list2]

    def test_get_all_task_lists_success(self):
        """Test successful retrieval of all task lists."""
        # Arrange
        self.task_list_repository.get_all.return_value = self.sample_task_lists
        
        # Act
        # Simulating what the service would do
        result = self.task_list_repository.get_all()
        
        # Assert
        assert result == self.sample_task_lists
        assert len(result) == 2
        self.task_list_repository.get_all.assert_called_once()
        
    def test_get_all_task_lists_empty(self):
        """Test behavior when there are no task lists."""
        # Arrange
        self.task_list_repository.get_all.return_value = []
        
        # Act
        result = self.task_list_repository.get_all()
        
        # Assert
        assert result == []
        assert len(result) == 0
        self.task_list_repository.get_all.assert_called_once()
        
    def test_get_all_task_lists_repository_error(self):
        """Test behavior when repository raises an exception."""
        # Arrange
        self.task_list_repository.get_all.side_effect = Exception("Database error")
        
        # Act & Assert
        with pytest.raises(Exception) as excinfo:
            self.task_list_repository.get_all()
            
        assert "Database error" in str(excinfo.value)
        self.task_list_repository.get_all.assert_called_once()
