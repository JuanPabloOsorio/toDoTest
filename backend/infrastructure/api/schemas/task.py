from datetime import datetime
from pydantic import BaseModel, Field
from pydantic.types import Base64Bytes
from typing import Optional

class TaskBaseSchema(BaseModel):
    id: str = Field(None, example="123e4567-e89b-12d3-a456-426614174000")
    title: str = Field(..., example="Complete project documentation")
    description: str = Field(..., example="Write the documentation for the new project features.")
    due_date: Optional[str] = Field(None, example="2023-12-31")
    list_id: str = Field(None, example="123e4567-e89b-12d3-a456-426614174000")
    created_at: Optional[str] = Field(None, example="2023-12-31")
    attachment: Optional[Base64Bytes] = Field(None, example=b"Sample attachment data")
    checklist: list = Field([], example=["Item 1", "Item 2"])
    owner: str = Field("default", example="user@example.com")
    done: bool = Field(False, example=False)
    order: int = Field(0, example=1, description="Order/position of the task in the list")

class TaskCreateSchema(BaseModel):
    title: str = Field(..., example="Complete project documentation")
    description: str = Field(..., example="Write the documentation for the new project features.")
    due_date: Optional[datetime] = Field(None, example="2023-12-31")
    list_id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")  # Required for creation
    attachment: Optional[Base64Bytes] = Field(None, example=b"Sample attachment data")
    checklist: Optional[list] = Field(None, example=["Item 1", "Item 2"])
    owner: str = Field("default", example="user@example.com")
    done: bool = Field(False, example=False)
    order: int = Field(0, example=1, description="Order/position of the task in the list")

class TaskUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, example="Complete project documentation")
    description: Optional[str] = Field(None, example="Write the documentation for the new project features.")
    due_date: Optional[datetime] = Field(None, example="2023-12-31")
    list_id: Optional[str] = Field(None, example="123e4567-e89b-12d3-a456-426614174000")
    attachment: Optional[Base64Bytes] = Field(None, example=b"Updated attachment data")
    checklist: Optional[list] = Field(None, example=["Item 1", "Item 2", "Item 3"])
    owner: Optional[str] = Field(None, example="user@example.com")
    done: Optional[bool] = Field(None, example=False)
    order: Optional[int] = Field(None, example=1, description="Order/position of the task in the list")

