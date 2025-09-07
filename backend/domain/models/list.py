from uuid import uuid4


class TaskList:
    def __init__(self, name: str, id: str = None):
        self.id = id if id else str(uuid4())
        if name in [None, ""]:
            raise Exception("Task List name could not be empty")
        self.name = name
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if not getattr(self, key):
                continue
            if key == "name":
                if value in [None, ""]:
                    raise Exception("error updating TaskList, name could not be None")
            setattr(self, key, value)

    @staticmethod
    def from_dict(data: dict):
        return  TaskList(
            id=data.get('id'),
            name=data.get('name')
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }