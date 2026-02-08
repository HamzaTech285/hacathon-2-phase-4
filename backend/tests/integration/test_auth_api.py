"""Integration tests for authentication API endpoints."""

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


def test_health_endpoint(client: TestClient):
    """Test the health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "message": "Todo App API is running"}


def test_signup_new_user(client: TestClient, session: Session):
    """Test signing up a new user."""
    signup_data = {
        "email": "test@example.com",
        "password": "securepassword123"
    }

    response = client.post("/api/auth/signup", json=signup_data)
    assert response.status_code == 200

    # Check that the response contains access token
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Verify user was created in the database
    user = session.exec(select(User).where(User.email == "test@example.com")).first()
    assert user is not None
    assert user.email == "test@example.com"


def test_signup_duplicate_email(client: TestClient):
    """Test signing up with an email that already exists."""
    # First signup
    signup_data = {
        "email": "duplicate@example.com",
        "password": "securepassword123"
    }

    response = client.post("/api/auth/signup", json=signup_data)
    assert response.status_code == 200

    # Second signup with same email
    response = client.post("/api/auth/signup", json=signup_data)
    assert response.status_code == 400  # Bad request due to duplicate email


def test_login_valid_credentials(client: TestClient):
    """Test logging in with valid credentials."""
    # First, create a user
    signup_data = {
        "email": "login_test@example.com",
        "password": "securepassword123"
    }

    signup_response = client.post("/api/auth/signup", json=signup_data)
    assert signup_response.status_code == 200

    # Now try to login
    login_data = {
        "email": "login_test@example.com",
        "password": "securepassword123"
    }

    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200

    # Check that the response contains access token
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    """Test logging in with invalid credentials."""
    # First, create a user
    signup_data = {
        "email": "invalid_login_test@example.com",
        "password": "securepassword123"
    }

    signup_response = client.post("/api/auth/signup", json=signup_data)
    assert signup_response.status_code == 200

    # Now try to login with wrong password
    login_data = {
        "email": "invalid_login_test@example.com",
        "password": "wrongpassword"
    }

    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 401  # Unauthorized


def test_login_nonexistent_user(client: TestClient):
    """Test logging in with a non-existent user."""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "any_password"
    }

    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 401  # Unauthorized


def test_signup_missing_fields(client: TestClient):
    """Test signing up with missing required fields."""
    # Missing email
    signup_data = {
        "password": "securepassword123"
    }

    response = client.post("/api/auth/signup", json=signup_data)
    assert response.status_code == 422  # Validation error

    # Missing password
    signup_data = {
        "email": "missing_field_test@example.com"
    }

    response = client.post("/api/auth/signup", json=signup_data)
    assert response.status_code == 422  # Validation error


def test_login_missing_fields(client: TestClient):
    """Test logging in with missing required fields."""
    # Missing email
    login_data = {
        "password": "any_password"
    }

    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 422  # Validation error

    # Missing password
    login_data = {
        "email": "missing_field_test@example.com"
    }

    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 422  # Validation error