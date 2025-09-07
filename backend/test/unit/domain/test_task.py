import pytest
from uuid import uuid4
from datetime import datetime, timedelta
from domain.models.task import Task

def test_task_initialization_minimal():
	new_task = Task(title="Test", list_id=str(uuid4()), description=None, created_at=None, due_date=None, attachment=None)
	assert new_task.title == "Test"
	assert new_task.description == ""
	assert isinstance(new_task.created_at, datetime)
	assert new_task.due_date is None
	assert new_task.attachment is None
	assert new_task.checklist == []
	assert new_task.owner == "default"
	assert new_task.done is False

def test_task_initialization_empty_title():
	with pytest.raises(Exception) as e:
		Task(title="", list_id=str(uuid4()), description="desc", created_at=datetime.now(), due_date=None, attachment=None)
	assert "Title of the Task could not be empty" in str(e.value)

def test_task_initialization_empty_list_id():
	with pytest.raises(Exception) as e:
		Task(title="Test", list_id="", description="desc", created_at=datetime.now(), due_date=None, attachment=None)
	assert "List ID of the Task could not be empty" in str(e.value)


def test_task_update_title():
	new_task = Task(title="A", list_id=str(uuid4()), description="desc", created_at=datetime.now(), due_date=None, attachment=None)
	new_task.update(title="B")
	assert new_task.title == "B"
	with pytest.raises(Exception):
		new_task.update(title="")

def test_task_update_list_id():
	new_task = Task(title="A", list_id=str(uuid4()), description="desc", created_at=datetime.now(), due_date=None, attachment=None)
	new_id = str(uuid4())
	new_task.update(list_id=new_id)
	assert new_task.list_id == new_id
	with pytest.raises(Exception):
		new_task.update(title="")

def test_task_update_owner():
	new_task = Task(title="A", list_id=str(uuid4()), description="desc", created_at=datetime.now(), due_date=None, attachment=None)
	new_task.update(owner="someone")
	assert new_task.owner == "someone"

def test_task_update_status():
	new_task = Task(title="A", list_id=str(uuid4()), description="desc", created_at=datetime.now(), due_date=None, attachment=None)
	new_task.update(done=True)
	assert new_task.done is True
	with pytest.raises(Exception):
		new_task.update(done="yes")

def test_task_update_due_date():
	new_task = Task(title="A", list_id=str(uuid4()), description="desc", created_at=datetime.now(), due_date=None, attachment=None)
	due_date = datetime.now() + timedelta(days=1)
	new_task.update(due_date=due_date)
	assert new_task.due_date == due_date
	with pytest.raises(Exception):
		new_task.update(due_date="tomorrow")

def test_task_update_attachment():
	new_task = Task(title="A", list_id=str(uuid4()), description="desc", created_at=datetime.now(), due_date=None, attachment=None)
	new_task.update(attachment=b"file")
	assert new_task.attachment == b"file"
	with pytest.raises(Exception):
		new_task.update(attachment="notbytes")

def test_task_update_checklist():
	new_task = Task(title="A", list_id=str(uuid4()), description="desc", created_at=datetime.now(), due_date=None, attachment=None)
	new_task.update(checklist=["item1", "item2"])
	assert new_task.checklist == ["item1", "item2"]
	with pytest.raises(Exception):
		new_task.update(checklist="notalist")

def test_task_update_description_none():
	new_task = Task(title="A", list_id=str(uuid4()), description="desc", created_at=datetime.now(), due_date=None, attachment=None)
	new_task.update(description=None)
	assert new_task.description == ""

def test_task_mark_complete_and_incomplete():
	new_task = Task(title="A", list_id=str(uuid4()), description="desc", created_at=datetime.now(), due_date=None, attachment=None)
	new_task.mark_complete()
	assert new_task.done is True
	new_task.mark_incomplete()
	assert new_task.done is False

def test_task_checklist_add_and_remove():
	new_task = Task(title="A", list_id=str(uuid4()), description="desc", created_at=datetime.now(), due_date=None, attachment=None)
	new_task.add_item_checklist("item1")
	assert "item1" in new_task.checklist
	with pytest.raises(Exception):
		new_task.add_item_checklist("")
	new_task.remove_item_from_checklist("item1")
	assert "item1" not in new_task.checklist
	with pytest.raises(Exception):
		new_task.remove_item_from_checklist("notfound")
