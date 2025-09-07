from datetime import datetime
from pydantic import BaseModel, Field
from pydantic.types import Base64Bytes

class TaskBaseSchema(BaseModel):
    id: str = Field(None, example="123e4567-e89b-12d3-a456-426614174000")
    title: str = Field(..., example="Complete project documentation")
    description: str = Field(..., example="Write the documentation for the new project features.")
    due_date: str = Field(None, example="2023-12-31")
    list_id: str = Field(None, example="123e4567-e89b-12d3-a456-426614174000")
    created_at: datetime = Field(None, example="2023-01-01T12:00:00Z")
    due_date: datetime = Field(None, example="2023-01-01T12:00:00Z")
    attachment: Base64Bytes | None = Field(None, example=b"Sample attachment data")
    checklist: list = Field([], example=["Item 1", "Item 2"])
    owner: str = Field("default", example="user@example.com")
    done: bool = Field(False, example=False)

class TaskCreateSchema(BaseModel):
    title: str = Field(..., example="Complete project documentation")
    description: str = Field(..., example="Write the documentation for the new project features.")
    due_date: datetime = Field(None, example="2023-01-01T12:00:00Z")
    list_id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")  # Required for creation
    attachment: Base64Bytes | None = Field(None, example=b"Sample attachment data")
    checklist: list = Field([], example=["Item 1", "Item 2"])
    owner: str = Field("default", example="user@example.com")
    done: bool = Field(False, example=False)

class TaskUpdateSchema(BaseModel):
    title: str | None = Field(None, example="Complete project documentation")
    description: str | None = Field(None, example="Write the documentation for the new project features.")
    due_date: datetime | None = Field(None, example="2023-01-01T12:00:00Z")
    list_id: str | None = Field(None, example="123e4567-e89b-12d3-a456-426614174000")
    attachment: Base64Bytes | None = Field(None, example=b"Updated attachment data")
    checklist: list | None = Field(None, example=["Item 1", "Item 2", "Item 3"])
    owner: str | None = Field(None, example="user@example.com")
    done: bool | None = Field(None, example=False)

