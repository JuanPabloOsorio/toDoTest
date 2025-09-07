import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4
from domain.models.list import TaskList
from infrastructure.repositories.json_task_list_repository import JsonTaskListRepository
from infrastructure.repositories.json_task_repository import JsonTaskRepository
import os
import json
import shutil
from datetime import datetime

client = TestClient(app)

# Use actual repositories but with test files
@pytest.fixture(scope="module")
def setup_test_environment():
    """Setup test environment with actual repositories pointing to test files"""
    # Create test data directory
    test_data_dir = "/tmp/toDoTest_test_data"
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
    
    # Patch the dependency functions
    dependencies.get_task_list_repo._task_list_repo_instance = task_list_repo
    dependencies.get_task_repo._task_repo_instance = task_repo
    
    # Setup initial test data
    test_list = TaskList(name="Test List")
    task_list_repo.save(test_list)
    
    yield task_list_repo, task_repo
    
    # Cleanup
    if os.path.exists(test_data_dir):
        shutil.rmtree(test_data_dir)
    
    # Restore original functions
    dependencies.get_task_list_repo._task_list_repo_instance = original_get_task_list_repo()
    dependencies.get_task_repo._task_repo_instance = original_get_task_repo()

class TestListsRoutes:
    
    def test_get_all_lists(self, setup_test_environment):
        """Test getting all lists"""
        task_list_repo, _ = setup_test_environment
        
        response = client.get("/lists/")
        assert response.status_code == 200
        data = response.json()
        assert data["successful"] is True
        # Should have our one test list
        assert len(data["data"]) >= 1
        
        # Check if our test list is in the results
        test_lists = [lst for lst in data["data"] if lst["name"] == "Test List"]
        assert len(test_lists) > 0
    
    def test_get_list_by_id(self, setup_test_environment):
        """Test getting a list by ID"""
        task_list_repo, _ = setup_test_environment
        
        # Get the lists to find a valid ID
        response = client.get("/lists/")
        data = response.json()
        
        # Get the first list ID
        list_id = data["data"][0]["id"]
        
        response = client.get(f"/lists/{list_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["successful"] is True
        assert data["data"]["id"] == list_id
    
    def test_get_list_by_invalid_id(self, setup_test_environment):
        """Test getting a list with an invalid ID"""
        invalid_id = str(uuid4())  # Generate a random ID that doesn't exist
        
        response = client.get(f"/lists/{invalid_id}")
        assert response.status_code == 500  # As per your implementation, it returns 500 for not found
        data = response.json()
        assert data["successful"] is False
        assert "Error getting" in data["error"]
    
    def test_create_list(self, setup_test_environment):
        """Test creating a new list"""
        task_list_repo, _ = setup_test_environment
        
        # Count existing lists
        response = client.get("/lists/")
        initial_count = len(response.json()["data"])
        
        new_list_data = {
            "name": f"New Test List {uuid4()}"  # Use UUID to ensure unique name
        }
        
        response = client.post("/lists/", json=new_list_data)
        assert response.status_code == 201
        data = response.json()
        assert data["successful"] is True
        assert data["data"]["name"] == new_list_data["name"]
        
        # Verify it was actually saved by checking count increased
        response = client.get("/lists/")
        new_count = len(response.json()["data"])
        assert new_count == initial_count + 1
    
    def test_update_list(self, setup_test_environment):
        """Test updating a list"""
        task_list_repo, _ = setup_test_environment
        
        # First create a new list specifically for this test
        new_list_data = {
            "name": f"Update Test List {uuid4()}"
        }
        
        create_response = client.post("/lists/", json=new_list_data)
        list_id = create_response.json()["data"]["id"]
        
        # Now update it
        update_data = {
            "name": f"Updated List {uuid4()}"
        }
        
        response = client.put(f"/lists/{list_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["successful"] is True
        assert data["data"]["name"] == update_data["name"]
        
        # Verify it was actually updated by getting it again
        response = client.get(f"/lists/{list_id}")
        assert response.json()["data"]["name"] == update_data["name"]
    
    def test_get_tasks_of_list_empty(self, setup_test_environment):
        """Test getting tasks of a list when empty"""
        task_list_repo, _ = setup_test_environment
        
        # First create a new list specifically for this test
        new_list_data = {
            "name": f"Tasks Test List {uuid4()}"
        }
        
        create_response = client.post("/lists/", json=new_list_data)
        list_id = create_response.json()["data"]["id"]
        
        # Get tasks for this list (should be empty)
        response = client.get(f"/lists/{list_id}/tasks")
        assert response.status_code == 200
        data = response.json()
        assert data["successful"] is True
        assert len(data["data"]) == 0  # No tasks yet
    
    def test_delete_list(self, setup_test_environment):
        """Test deleting a list"""
        task_list_repo, _ = setup_test_environment
        
        # First create a new list specifically for this test
        new_list_data = {
            "name": f"Delete Test List {uuid4()}"
        }
        
        create_response = client.post("/lists/", json=new_list_data)
        list_id = create_response.json()["data"]["id"]
        
        # Now delete it
        response = client.delete(f"/lists/{list_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["successful"] is True
        
        # Verify it was actually deleted by trying to get it
        response = client.get(f"/lists/{list_id}")
        assert response.status_code == 500  # Not found returns 500 in your implementation
