from datetime import datetime
from uuid import uuid4

class Task:
    def __init__(
            self,
            title: str,
            list_id: str,
            description: str | None,
            due_date: datetime | None,
            attachment: bytes | bytearray | None,
            created_at: datetime | None = None,
            checklist: list = [],
            id: str = None,
            owner: str = None,
            done: bool = False,
            order: int = 0,
    ):
        if title in ["", None]:
            raise Exception("Title of the Task could not be empty")
        if list_id in ["", None]:
            raise Exception("List ID of the Task could not be empty")

        self.id = id if id else str(uuid4())
        self.title = title
        self.list_id = list_id
        self.description = description if description else ""
        self.created_at = created_at if created_at else datetime.now()
        self.due_date = due_date if due_date else None
        self.attachment = attachment
        self.checklist = checklist if checklist else []
        self.owner = owner if owner else 'default'
        self.done = done if done else False
        self.order = order
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            # Only update attributes that exist on the object
            if not hasattr(self, key):
                continue
            if key == "title":
                if value in ["", None]:
                    raise Exception(f"Title of the Task could not be empty")
            if key == "list_id":
                if value in ["", None]:
                    raise Exception(f"List ID of the Task could not be empty")
            # Skip updating immutable fields
            if key in ["created_at", "id"]:
                continue
            if key == "owner":
                if value in ["", None]:
                    raise Exception(f"Owner of the Task could not be empty")
            if key == "done":
                if not isinstance(value, bool):
                    raise Exception(f"Status of the Task must be a True or False")
            if key == "due_date":
                if value and not isinstance(value, datetime):
                    raise Exception(f"Due date of the Task must be a datetime object")
            if key == "attachment":
                if value and not isinstance(value, (bytes, bytearray)):
                    raise Exception(f"Attachment of the Task must be bytes or bytearray")
            if key == "checklist":
                if value and not isinstance(value, list):
                    raise Exception(f"Checklist of the Task must be a list")
            if key == "order":
                if value is not None and not isinstance(value, int):
                    raise Exception(f"Order of the Task must be an integer")
            if key == "description":
                if value is None:
                    value = ""
            setattr(self, key, value)
    
    def mark_complete(self):
        self.done = True
    
    def mark_incomplete(self):
        self.done = False
    
    def add_item_checklist(self, item: str):
        if item in ["", None]:
            raise Exception("Checklist item could not be empty")
        self.checklist.append(item)
    
    def remove_item_from_checklist(self, item: str):
        if item in self.checklist:
            self.checklist.remove(item)
        else:
            raise Exception("Checklist item not found")
    
    @staticmethod
    def from_dict(data: dict):
        if data.get('created_at'):
            try:
                created_at = datetime.strptime(data['created_at'], '%Y-%m-%d')
            except ValueError:
                # Fallback to ISO format if the simple format fails
                created_at = datetime.fromisoformat(data['created_at'])
        else:
            raise ValueError("created_at is required in data")
        
        # Parse due_date as YYYY-MM-DD format
        due_date = None
        if data.get('due_date'):
            try:
                due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
            except ValueError:
                # Fallback to ISO format if the simple format fails
                due_date = datetime.fromisoformat(data['due_date'])
                
        return Task(
            title=data['title'],
            description=data.get('description'),
            list_id=data.get('list_id'),
            due_date=due_date,
            attachment=data.get('attachment').encode('utf-8') if data.get('attachment') else None,
            checklist=data.get('checklist', []),
            created_at=created_at,
            owner=data.get('owner', 'default'),
            id=data.get('id'),
            done=data.get('done', False),
            order=data.get('order', 0)
        )

    def to_dict(self):
        """
        Convert the Task object to a dictionary for JSON serialization.
        """
        return {
            "id": self.id,
            "title": self.title,
            "list_id": self.list_id,
            "description": self.description,
            "created_at": self.created_at.strftime('%Y-%m-%d') if self.created_at else None,
            "due_date": self.due_date.strftime('%Y-%m-%d') if self.due_date else None,
            "attachment": self.attachment.decode('utf-8') if self.attachment else None,
            "checklist": self.checklist,
            "owner": self.owner,
            "done": self.done,
            "order": self.order
        }
