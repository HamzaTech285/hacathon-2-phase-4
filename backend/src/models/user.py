from __future__ import annotations
"""User model for the Todo App."""

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from sqlalchemy.orm import RelationshipProperty
from typing import TYPE_CHECKING, Optional, List
from datetime import datetime
from enum import Enum

if TYPE_CHECKING:
    from .task import Task


class UserRole(str, Enum):
    """User roles for authorization."""
    USER = "user"
    ADMIN = "admin"


class UserBase(SQLModel):
    """Base class for User model with common fields."""
    email: str


class User(UserBase, table=True):
    """User model representing application users."""
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(sa_column_kwargs={"unique": True, "nullable": False})
    password_hash: str = Field(sa_column_kwargs={"nullable": False})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    role: UserRole = Field(default=UserRole.USER)

    # Relationship to tasks
    # Relationship to tasks
    # tasks: list["Task"] = Relationship(back_populates="user")


class UserRead(UserBase):
    """Schema for reading user data."""
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    role: UserRole


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str
    email: str


class UserUpdate(SQLModel):
    """Schema for updating user data."""
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UserLogin(SQLModel):
    """Schema for user login."""
    email: str
    password: str