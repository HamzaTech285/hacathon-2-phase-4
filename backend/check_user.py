"""
Script to check if the test user exists in the database.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from sqlmodel import create_engine, Session, select
from src.models.user import User
from src.database import DATABASE_URL

def check_user():
    engine = create_engine(DATABASE_URL)
    
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == "test@example.com")).first()
        
        if user:
            print(f"User found: {user.email}")
            print(f"User ID: {user.id}")
            print(f"Is active: {user.is_active}")
            print(f"Created at: {user.created_at}")
        else:
            print("No user found with email test@example.com")

if __name__ == "__main__":
    check_user()