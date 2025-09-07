import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4
from domain.models.task import Task
from domain.models.list import TaskList
from infrastructure.repositories.json_task_repository import JsonTaskRepository
from infrastructure.repositories.json_task_list_repository import JsonTaskListRepository
import os
import json
import shutil
from datetime import datetime

client = TestClient(app)

# Use actual repositories but with test files
@pytest.fixture(scope="function")
def setup_test_environment():
    """Setup test environment with actual repositories pointing to test files"""
    # Create test data directory
    test_data_dir = "/tmp/toDoTest_task_test_data"
    if os.path.exists(test_data_dir):
        shutil.rmtree(test_data_dir)
    os.makedirs(test_data_dir)
    
    # Create test files
    task_lists_file = os.path.join(test_data_dir, "task_lists.json")
    tasks_file = os.path.join(test_data_dir, "tasks.json")
    
    # Initialize empty files
    with open(task_lists_file, "w") as f:
        json.dump([], f)
    
    with open(tasks_file, "w") as f:
        json.dump([], f)
    
    # Patch the dependency injection to use our test files
    import dependencies.get_task_list_repo
    import dependencies.get_task_repo
    
    # Store original functions
    original_get_task_list_repo = dependencies.get_task_list_repo.get_task_list_repository
    original_get_task_repo = dependencies.get_task_repo.get_task_repository
    
    # Create test repositories
    task_list_repo = JsonTaskListRepository(file_path=task_lists_file)
    task_repo = JsonTaskRepository(file_path=tasks_file)
    
    # Add test data
    test_list = TaskList(name="Test List")
    test_list.id = "test-list-id"  # Fixed ID for testing
    task_list_repo.save(test_list)
    
    test_task = Task(
        title="Test Task",
        description="Test Description",
        list_id="test-list-id",
        due_date=None,
        attachment=None,
        created_at=datetime.now()
    )
    task_repo.save(test_task)
    
    # Patch the dependency functions
    dependencies.get_task_list_repo._task_list_repo_instance = task_list_repo
    dependencies.get_task_repo._task_repo_instance = task_repo
    
    # Yield test data and repositories
    yield {
        "task_repo": task_repo,
        "task_list_repo": task_list_repo,
        "test_dir": test_data_dir,
        "test_task_id": test_task.id,
        "test_list_id": test_list.id
    }
    
    # Restore original functions
    dependencies.get_task_list_repo._task_list_repo_instance = original_get_task_list_repo()
    dependencies.get_task_repo._task_repo_instance = original_get_task_repo()
    
    # Cleanup
    if os.path.exists(test_data_dir):
        shutil.rmtree(test_data_dir)

class TestTaskRoutes:
    
    def test_get_task(self, setup_test_environment):
        """Test getting a task by ID"""
        test_task_id = setup_test_environment["test_task_id"]
        
        response = client.get(f"/task/{test_task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["successful"] is True
        assert data["data"]["id"] == test_task_id
        assert data["data"]["title"] == "Test Task"
    
    def test_get_task_invalid_id(self, setup_test_environment):
        """Test getting a task with an invalid ID"""
        invalid_id = str(uuid4())  # Generate a random ID that doesn't exist
        
        response = client.get(f"/task/{invalid_id}")
        assert response.status_code == 500  # As per your implementation, it returns 500 for not found
        data = response.json()
        assert data["successful"] is False
        assert "Error getting" in data["error"]
    
    def test_create_task(self, setup_test_environment):
        """Test creating a new task"""
        test_list_id = setup_test_environment["test_list_id"]
        
        # Due date as None doesn't work with Pydantic validation, so we omit it entirely
        new_task_data = {
            "title": "New Test Task",
            "description": "New Test Description",
            "list_id": test_list_id,
            "attachment": None,
            "checklist": ["Item 1", "Item 2"],
            "owner": "test-user",
            "done": False
        }
        
        response = client.post("/task/", json=new_task_data)
        print(f"Response for create_task: {response.text}")
        assert response.status_code == 201
        data = response.json()
        assert data["successful"] is True
        assert data["data"]["title"] == "New Test Task"
        assert data["data"]["list_id"] == test_list_id
    
    def test_update_task(self, setup_test_environment):
        """Test updating a task"""
        test_task_id = setup_test_environment["test_task_id"]
        task_repo = setup_test_environment["task_repo"]
        
        update_data = {
            "title": "Updated Test Task",
            "done": True
        }
        
        response = client.put(f"/task/{test_task_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["successful"] is True
        assert data["data"]["title"] == "Updated Test Task"
        assert data["data"]["done"] is True
        
        # Verify it was actually updated
        updated_task = task_repo.get_by_id(test_task_id)
        assert updated_task.title == "Updated Test Task"
        assert updated_task.done is True
    
    def test_delete_task(self, setup_test_environment):
        """Test deleting a task"""
        test_task_id = setup_test_environment["test_task_id"]
        task_repo = setup_test_environment["task_repo"]
        
        response = client.delete(f"/task/{test_task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["successful"] is True
        assert data["message"] == "Task deleted successfully"
        
        # Verify it was actually deleted - it should be gone from the repository
        assert test_task_id not in task_repo.tasks
            
    def test_get_tasks_by_list(self, setup_test_environment):
        """Test getting all tasks for a specific list"""
        test_list_id = setup_test_environment["test_list_id"]
        
        # Get tasks for this list
        response = client.get(f"/lists/{test_list_id}/tasks")
        assert response.status_code == 200
        data = response.json()
        assert data["successful"] is True
        
        # Should find at least our test task
        assert len(data["data"]) >= 1
        
        # Check if all returned tasks have the correct list_id
        for task in data["data"]:
            assert task["list_id"] == test_list_id
