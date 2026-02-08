#!/usr/bin/env python3
"""
Script to initialize the database by creating all tables.
"""

from sqlmodel import SQLModel
from src.database import engine

def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    
    # Import models inside the function to avoid early validation
    from src.models.user import User
    from src.models.task import Task
    
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()