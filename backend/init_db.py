#!/usr/bin/env python3
"""
Script to initialize the database by creating all tables.
"""

from sqlmodel import SQLModel
from src.database import engine
from src.models.user import User
from src.models.task import Task  # Import all models to register them with SQLModel

def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()