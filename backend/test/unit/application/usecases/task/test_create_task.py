import pytest
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime
from application.usecases.task.create_task import CreateTaskService
from domain.models.list import TaskList
from domain.models.task import Task

class TestCreateTaskService:
    def setup_method(self):
        """Setup for each test."""
        self.task_repository = Mock()
        self.task_list_repository = Mock()
        self.service = CreateTaskService(self.task_repository, self.task_list_repository)
        
        # Sample task data
        self.list_id = str(uuid4())
        self.title = "Test Task"
        self.description = "Test Description"
        self.created_at = datetime.now()
        self.due_date = None
        self.attachment = None
        self.checklist = []
        self.owner = "test_owner"
        self.done = False

    def test_create_task_success(self):
        """Test successful creation of a task."""

        task_list = TaskList(name="Sample List", id=self.list_id)
        # Arrange
        task = Task(
            title=self.title,
            list_id=self.list_id,
            description=self.description,
            created_at=self.created_at,
            due_date=self.due_date,
            attachment=self.attachment,
            checklist=self.checklist,
            owner=self.owner,
            done=self.done
        )
        self.task_repository.save.return_value = task
        self.task_list_repository.get_by_id.return_value = task_list
        
        # Act
        result = self.service.execute(
            title=self.title,
            list_id=self.list_id,
            description=self.description,
            due_date=self.due_date,
            attachment=self.attachment,
            checklist=self.checklist,
            owner=self.owner,
            done=self.done
        )
        
        # Assert
        self.task_repository.save.assert_called_once()
        assert result.title == self.title
        assert result.list_id == self.list_id
        assert result.description == self.description
        assert result.due_date == self.due_date
        assert result.attachment == self.attachment
        assert result.checklist == self.checklist
        assert result.owner == self.owner
        assert result.done == self.done
        
    def test_create_task_invalid_data(self):
        """Test behavior when task data is invalid."""
        # Arrange - empty title should raise an exception
        invalid_title = ""
        
        # Act & Assert
        with pytest.raises(Exception) as excinfo:
            self.service.execute(
                title=invalid_title,
                list_id=self.list_id,
                description=self.description,
                due_date=self.due_date,
                attachment=self.attachment,
                checklist=self.checklist,
                owner=self.owner,
                done=self.done
            )
            
        assert "Title of the Task could not be empty" in str(excinfo.value)
        self.task_repository.save.assert_not_called()
        
    def test_create_task_invalid_list_id(self):
        """Test behavior when list_id is invalid."""
        # Arrange - empty list_id should raise an exception
        invalid_list_id = ""
        self.task_list_repository.get_by_id.return_value = None
        # Act & Assert
        with pytest.raises(Exception) as excinfo:
            self.service.execute(
                title=self.title,
                list_id=invalid_list_id,
                description=self.description,
                due_date=self.due_date,
                attachment=self.attachment,
                checklist=self.checklist,
                owner=self.owner,
                done=self.done
            )
            
        assert f"Task list with ID {invalid_list_id} does not exist." in str(excinfo.value)
        self.task_repository.save.assert_not_called()
        
    def test_create_task_repository_error(self):
        """Test behavior when repository raises an exception."""
        # Arrange
        self.task_repository.save.side_effect = Exception("Database error")
        
        # Act & Assert
        with pytest.raises(Exception) as excinfo:
            self.service.execute(
                title=self.title,
                list_id=self.list_id,
                description=self.description,
                due_date=self.due_date,
                attachment=self.attachment,
                checklist=self.checklist,
                owner=self.owner,
                done=self.done
            )
            
        assert "Database error" in str(excinfo.value)
        self.task_repository.save.assert_called_once()
