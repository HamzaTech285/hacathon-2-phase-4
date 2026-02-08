from __future__ import annotations
"""
Database configuration and session management for the Todo App.
"""
from sqlmodel import create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# For Neon PostgreSQL, you might need to add connection parameters
if "neon" in DATABASE_URL:
    connect_args = {"sslmode": "require"}
else:
    connect_args = {}

engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)


def get_session() -> Generator[Session, None, None]:
    """
    Get database session for dependency injection.
    """
    with Session(engine) as session:
        yield session