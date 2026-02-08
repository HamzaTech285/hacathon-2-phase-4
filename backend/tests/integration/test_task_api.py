"""Integration tests for task API endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel, select
from sqlmodel.pool import StaticPool
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.main import app
from src.database import get_session
from src.models.user import User
from src.models.task import Task
from src.auth_handler import get_password_hash


# Create an in-memory SQLite database for testing
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="authenticated_client")
def authenticated_client_fixture(client: TestClient, session: Session):
    # Create a test user
    user_data = User(
        email="testuser@example.com",
        password_hash=get_password_hash("testpassword123"),
        is_active=True
    )
    session.add(user_data)
    session.commit()
    session.refresh(user_data)

    # Login to get a token
    login_data = {
        "email": "testuser@example.com",
        "password": "testpassword123"
    }

    login_response = client.post("/api/auth/login", json=login_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Add the token to the client headers
    client.headers.update({"Authorization": f"Bearer {token}"})

    # Add the user_id to the fixture for later use
    client.user_id = user_data.id

    return client


def test_get_tasks_unauthenticated(client: TestClient):
    """Test that getting tasks requires authentication."""
    response = client.get("/api/tasks")
    assert response.status_code == 401  # Unauthorized


def test_create_task_unauthenticated(client: TestClient):
    """Test that creating a task requires authentication."""
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "user_id": 1
    }

    response = client.post("/api/tasks", json=task_data)
    assert response.status_code == 401  # Unauthorized


def test_get_tasks_authenticated_empty(authenticated_client: TestClient):
    """Test getting tasks for an authenticated user (empty list)."""
    response = authenticated_client.get("/api/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_create_task_authenticated(authenticated_client: TestClient, session: Session):
    """Test creating a task for an authenticated user."""
    task_data = {
        "title": "Test Task",
        "description": "Test Description"
    }

    response = authenticated_client.post("/api/tasks", json=task_data)
    assert response.status_code == 200

    # Check that the response contains the created task
    created_task = response.json()
    assert created_task["title"] == "Test Task"
    assert created_task["description"] == "Test Description"
    assert "id" in created_task

    # Verify the task was saved to the database
    saved_task = session.get(Task, created_task["id"])
    assert saved_task is not None
    assert saved_task.title == "Test Task"
    assert saved_task.user_id == authenticated_client.user_id  # Should match the authenticated user


def test_get_specific_task_authenticated(authenticated_client: TestClient):
    """Test getting a specific task for an authenticated user."""
    # First, create a task
    task_data = {
        "title": "Specific Task",
        "description": "Test Description"
    }

    create_response = authenticated_client.post("/api/tasks", json=task_data)
    assert create_response.status_code == 200
    created_task = create_response.json()

    # Now get the specific task
    response = authenticated_client.get(f"/api/tasks/{created_task['id']}")
    assert response.status_code == 200

    retrieved_task = response.json()
    assert retrieved_task["id"] == created_task["id"]
    assert retrieved_task["title"] == "Specific Task"


def test_update_task_authenticated(authenticated_client: TestClient):
    """Test updating a task for an authenticated user."""
    # First, create a task
    task_data = {
        "title": "Original Task",
        "description": "Original Description"
    }

    create_response = authenticated_client.post("/api/tasks", json=task_data)
    assert create_response.status_code == 200
    created_task = create_response.json()

    # Now update the task
    update_data = {
        "title": "Updated Task",
        "description": "Updated Description",
        "is_completed": True
    }

    response = authenticated_client.put(f"/api/tasks/{created_task['id']}", json=update_data)
    assert response.status_code == 200

    updated_task = response.json()
    assert updated_task["id"] == created_task["id"]
    assert updated_task["title"] == "Updated Task"
    assert updated_task["description"] == "Updated Description"
    assert updated_task["is_completed"] is True


def test_delete_task_authenticated(authenticated_client: TestClient, session: Session):
    """Test deleting a task for an authenticated user."""
    # First, create a task
    task_data = {
        "title": "Task to Delete",
        "description": "Will be deleted"
    }

    create_response = authenticated_client.post("/api/tasks", json=task_data)
    assert create_response.status_code == 200
    created_task = create_response.json()

    # Verify the task exists
    get_response = authenticated_client.get(f"/api/tasks/{created_task['id']}")
    assert get_response.status_code == 200

    # Now delete the task
    response = authenticated_client.delete(f"/api/tasks/{created_task['id']}")
    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted successfully"}

    # Verify the task no longer exists
    get_response = authenticated_client.get(f"/api/tasks/{created_task['id']}")
    assert get_response.status_code == 404


def test_get_tasks_with_completion_filter(authenticated_client: TestClient):
    """Test getting tasks with completion filter."""
    # Create some tasks
    task1_data = {"title": "Incomplete Task", "description": "Not done yet"}
    task2_data = {"title": "Complete Task", "description": "Already done", "is_completed": True}

    response1 = authenticated_client.post("/api/tasks", json=task1_data)
    response2 = authenticated_client.post("/api/tasks", json=task2_data)

    assert response1.status_code == 200
    assert response2.status_code == 200

    # Get all tasks
    all_tasks_response = authenticated_client.get("/api/tasks")
    assert all_tasks_response.status_code == 200
    all_tasks = all_tasks_response.json()
    assert len(all_tasks) >= 2

    # Get only completed tasks
    completed_tasks_response = authenticated_client.get("/api/tasks?completed=true")
    assert completed_tasks_response.status_code == 200
    completed_tasks = completed_tasks_response.json()

    # Check that all returned tasks are completed
    for task in completed_tasks:
        assert task["is_completed"] is True

    # Get only incomplete tasks
    incomplete_tasks_response = authenticated_client.get("/api/tasks?completed=false")
    assert incomplete_tasks_response.status_code == 200
    incomplete_tasks = incomplete_tasks_response.json()

    # Check that all returned tasks are not completed
    for task in incomplete_tasks:
        assert task["is_completed"] is False


def test_update_nonexistent_task(authenticated_client: TestClient):
    """Test updating a non-existent task."""
    update_data = {"title": "Updated Title"}

    response = authenticated_client.put("/api/tasks/99999", json=update_data)
    assert response.status_code == 404


def test_get_nonexistent_task(authenticated_client: TestClient):
    """Test getting a non-existent task."""
    response = authenticated_client.get("/api/tasks/99999")
    assert response.status_code == 404


def test_delete_nonexistent_task(authenticated_client: TestClient):
    """Test deleting a non-existent task."""
    response = authenticated_client.delete("/api/tasks/99999")
    assert response.status_code == 404