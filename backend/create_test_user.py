"""
Script to create a test user for the Todo App.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from sqlmodel import SQLModel, Field, create_engine, Session
from src.models.user import User
from src.auth_handler import get_password_hash
from src.database import DATABASE_URL

def create_test_user():
    engine = create_engine(DATABASE_URL)
    
    # Create tables if they don't exist
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        # Check if user already exists
        existing_user = session.query(User).filter(User.email == "test@example.com").first()
        
        if existing_user:
            print("Test user already exists!")
            print(f"Email: {existing_user.email}")
            print(f"ID: {existing_user.id}")
            return
        
        # Create a new test user
        hashed_password = get_password_hash("password123")
        test_user = User(
            email="test@example.com",
            password_hash=hashed_password,
            is_active=True
        )
        
        session.add(test_user)
        session.commit()
        session.refresh(test_user)
        
        print("Test user created successfully!")
        print(f"Email: {test_user.email}")
        print(f"Password: password123")
        print(f"ID: {test_user.id}")

if __name__ == "__main__":
    create_test_user()