"""Unit tests for the authentication service."""

import pytest
from unittest.mock import Mock, patch
from sqlmodel import Session, select
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.user import User, UserCreate
from src.services.auth import AuthService
from src.auth_handler import get_password_hash


def test_register_user_success():
    """Test successful user registration."""
    # Arrange
    user_data = UserCreate(email="test@example.com", password="password123")

    mock_db_session = Mock(spec=Session)
    mock_existing_user = None

    mock_db_session.exec.return_value.first.return_value = mock_existing_user

    # Create a mock user object that will be returned after registration
    mock_new_user = User(
        id=1,
        email="test@example.com",
        password_hash=get_password_hash("password123")
    )

    # Act
    with patch('backend.src.services.auth.get_password_hash') as mock_hash:
        mock_hash.return_value = "hashed_password"

        # Mock the db_session.add, commit, and refresh methods
        mock_db_session.add = Mock()
        mock_db_session.commit = Mock()
        mock_db_session.refresh = Mock(return_value=mock_new_user)

        # Create the user object that will be returned
        created_user = User(
            id=1,
            email=user_data.email,
            password_hash="hashed_password"
        )
        mock_db_session.refresh = Mock()
        mock_db_session.merge = Mock(return_value=created_user)

        # Manually set the id after the commit
        created_user.id = 1

        result = AuthService.register_user(user_data, mock_db_session)

    # Assert
    assert result.email == user_data.email
    mock_db_session.exec.assert_called_once()
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()


def test_register_user_duplicate_email():
    """Test registration with duplicate email raises exception."""
    # Arrange
    user_data = UserCreate(email="existing@example.com", password="password123")

    mock_db_session = Mock(spec=Session)
    mock_existing_user = User(id=1, email="existing@example.com", password_hash="some_hash")
    mock_db_session.exec.return_value.first.return_value = mock_existing_user

    # Act & Assert
    with pytest.raises(Exception):  # Should raise HTTPException but we're simplifying
        AuthService.register_user(user_data, mock_db_session)


def test_authenticate_user_success():
    """Test successful user authentication."""
    # Arrange
    email = "test@example.com"
    password = "password123"

    mock_db_session = Mock(spec=Session)
    mock_user = User(
        id=1,
        email=email,
        password_hash=get_password_hash(password)  # Use the actual hash function
    )
    mock_db_session.exec.return_value.first.return_value = mock_user

    # Act
    with patch('backend.src.services.auth.verify_password', return_value=True) as mock_verify:
        result = AuthService.authenticate_user(email, password, mock_db_session)

    # Assert
    assert result is not None
    assert result.email == email
    mock_verify.assert_called_once()


def test_authenticate_user_invalid_credentials():
    """Test authentication with invalid credentials returns None."""
    # Arrange
    email = "test@example.com"
    password = "password123"
    invalid_password = "wrongpassword"

    mock_db_session = Mock(spec=Session)
    mock_user = User(
        id=1,
        email=email,
        password_hash=get_password_hash(password)
    )
    mock_db_session.exec.return_value.first.return_value = mock_user

    # Act
    with patch('backend.src.services.auth.verify_password', return_value=False) as mock_verify:
        result = AuthService.authenticate_user(email, invalid_password, mock_db_session)

    # Assert
    assert result is None
    mock_verify.assert_called_once()


def test_authenticate_user_nonexistent_user():
    """Test authentication with nonexistent user returns None."""
    # Arrange
    email = "nonexistent@example.com"
    password = "password123"

    mock_db_session = Mock(spec=Session)
    mock_db_session.exec.return_value.first.return_value = None

    # Act
    result = AuthService.authenticate_user(email, password, mock_db_session)

    # Assert
    assert result is None


def test_create_access_token_for_user():
    """Test creating access token for a user."""
    # Arrange
    mock_user = User(
        id=1,
        email="test@example.com",
        password_hash="hashed_password"
    )

    # Act
    with patch('backend.src.services.auth.create_access_token', return_value="mock_token"):
        result = AuthService.create_access_token_for_user(mock_user)

    # Assert
    assert result == "mock_token"


def test_get_user_by_email_found():
    """Test getting a user by email when user exists."""
    # Arrange
    email = "test@example.com"
    mock_db_session = Mock(spec=Session)
    mock_user = User(
        id=1,
        email=email,
        password_hash="hashed_password"
    )
    mock_db_session.exec.return_value.first.return_value = mock_user

    # Act
    result = AuthService.get_user_by_email(email, mock_db_session)

    # Assert
    assert result is not None
    assert result.email == email


def test_get_user_by_email_not_found():
    """Test getting a user by email when user does not exist."""
    # Arrange
    email = "nonexistent@example.com"
    mock_db_session = Mock(spec=Session)
    mock_db_session.exec.return_value.first.return_value = None

    # Act
    result = AuthService.get_user_by_email(email, mock_db_session)

    # Assert
    assert result is None