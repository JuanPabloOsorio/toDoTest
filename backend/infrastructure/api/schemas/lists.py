from datetime import datetime
from pydantic import BaseModel, Field

class TaskListBaseSchema(BaseModel):
    id: str = Field(None, example="123e4567-e89b-12d3-a456-426614174000")
    name: str = Field(..., example="To Do")


class TaskListCreateSchema(BaseModel):
    name: str = Field(..., example="To Do")

class TaskListUpdateSchema(TaskListCreateSchema):
    ...
