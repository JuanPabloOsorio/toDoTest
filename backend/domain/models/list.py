from uuid import uuid4


class TaskList:
    def __init__(self, name: str, id: str = None, order: int = 0):
        self.id = id if id else str(uuid4())
        if name in [None, ""]:
            raise Exception("Task List name could not be empty")
        self.name = name
        self.order = order
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            # Only update attributes that exist on the object
            if not hasattr(self, key):
                continue
            if key == "name":
                if value in [None, ""]:
                    raise Exception("error updating TaskList, name could not be None")
            if key == "order":
                if value is not None and not isinstance(value, int):
                    raise Exception("error updating TaskList, order must be an integer")
            setattr(self, key, value)

    @staticmethod
    def from_dict(data: dict):
        return  TaskList(
            id=data.get('id'),
            name=data.get('name'),
            order=data.get('order', 0)
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "order": self.order
        }