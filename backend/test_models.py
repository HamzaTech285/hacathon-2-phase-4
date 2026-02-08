#!/usr/bin/env python3
"""
Simple test to check if models can be imported without error.
"""

print("Attempting to import models...")

try:
    from sqlmodel import SQLModel, Field
    print("[OK] SQLModel imported successfully")
except ImportError as e:
    print(f"[ERROR] Error importing SQLModel: {e}")
    exit(1)

try:
    from src.models.user import User
    print("[OK] User model imported successfully")
except Exception as e:
    print(f"[ERROR] Error importing User model: {e}")
    exit(1)

try:
    from src.models.task import Task
    print("[OK] Task model imported successfully")
except Exception as e:
    print(f"[ERROR] Error importing Task model: {e}")
    exit(1)

print("[OK] All models imported successfully!")