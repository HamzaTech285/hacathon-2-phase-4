from __future__ import annotations
"""Conversation and Message models for chat functionality."""

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON
from typing import Optional
from datetime import datetime


class Conversation(SQLModel, table=True):
    """Conversation model for storing chat sessions."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", sa_column_kwargs={"nullable": False})
    title: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Message(SQLModel, table=True):
    """Message model for storing chat messages."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", sa_column_kwargs={"nullable": False})
    role: str = Field(sa_column_kwargs={"nullable": False})
    content: str = Field(sa_column_kwargs={"nullable": False})
    tool_calls: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
