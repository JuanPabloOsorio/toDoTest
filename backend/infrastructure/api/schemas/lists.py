from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class TaskListBaseSchema(BaseModel):
    id: str = Field(None, example="123e4567-e89b-12d3-a456-426614174000")
    name: str = Field(..., example="To Do")
    order: int = Field(0, example=1, description="Order/position of the list")


class TaskListCreateSchema(BaseModel):
    name: str = Field(..., example="To Do")
    order: int = Field(0, example=1, description="Order/position of the list")

class TaskListUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, example="To Do")
    order: Optional[int] = Field(None, example=1, description="Order/position of the list")
