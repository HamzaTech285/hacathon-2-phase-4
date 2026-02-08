from __future__ import annotations
"""Task model for the Todo App."""

from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional
from datetime import datetime

if TYPE_CHECKING:
    from .user import User


class TaskBase(SQLModel):
    """Base class for Task model with common fields."""
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    due_date: Optional[datetime] = None


class Task(TaskBase, table=True):
    """Task model representing user tasks."""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(sa_column_kwargs={"nullable": False})
    user_id: int = Field(foreign_key="user.id", sa_column_kwargs={"nullable": False})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    # user: "User" = Relationship(back_populates="tasks")


class TaskRead(TaskBase):
    """Schema for reading task data."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    title: str
    user_id: int


class TaskUpdate(SQLModel):
    """Schema for updating task data."""
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None