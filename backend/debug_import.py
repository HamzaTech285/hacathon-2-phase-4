from __future__ import annotations
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

print("Attempting to import models...")
try:
    from src.models.user import User, UserCreate, UserLogin
    from src.models.task import Task, TaskCreate
    print("Models imported successfully")
except Exception as e:
    print(f"Failed to import models: {e}")
    import traceback
    traceback.print_exc()

print("\nAttempting to import routers...")
try:
    from src.api.auth_router import auth_router
    from src.api.task_router import task_router
    print("Routers imported successfully")
except Exception as e:
    print(f"Failed to import routers: {e}")
    import traceback
    traceback.print_exc()

print("\nAttempting to import app...")
try:
    from src.main import app
    print("App imported successfully")
except Exception as e:
    print(f"Failed to import app: {e}")
    import traceback
    traceback.print_exc()
