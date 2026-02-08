"""Unit tests for the task service."""

import pytest
from unittest.mock import Mock, patch
from sqlmodel import Session
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.task import Task, TaskCreate, TaskUpdate
from src.models.user import User
from src.services.task_service import TaskService


def test_create_task_success():
    """Test successful task creation."""
    # Arrange
    user_id = 1
    task_data = TaskCreate(
        title="Test Task",
        description="Test Description",
        user_id=user_id
    )

    mock_db_session = Mock(spec=Session)
    mock_user = User(
        id=user_id,
        email="test@example.com",
        password_hash="hashed_password"
    )

    # Mock the session.get method to return the user
    mock_db_session.get.return_value = mock_user

    # Mock the task creation process
    created_task = Task(
        id=1,
        title=task_data.title,
        description=task_data.description,
        user_id=task_data.user_id,
        is_completed=False
    )

    mock_db_session.add = Mock()
    mock_db_session.commit = Mock()
    mock_db_session.refresh = Mock()

    # Act
    result = TaskService.create_task(task_data, mock_db_session)

    # Assert
    assert result.title == task_data.title
    assert result.user_id == task_data.user_id
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()


def test_create_task_user_not_found():
    """Test task creation fails when user doesn't exist."""
    # Arrange
    user_id = 999  # Non-existent user ID
    task_data = TaskCreate(
        title="Test Task",
        description="Test Description",
        user_id=user_id
    )

    mock_db_session = Mock(spec=Session)
    mock_db_session.get.return_value = None  # User not found

    # Act & Assert
    with pytest.raises(Exception):  # Should raise HTTPException
        TaskService.create_task(task_data, mock_db_session)


def test_get_task_by_id_success():
    """Test successful retrieval of a task by ID."""
    # Arrange
    task_id = 1
    user_id = 1
    mock_db_session = Mock(spec=Session)

    mock_task = Task(
        id=task_id,
        title="Test Task",
        description="Test Description",
        user_id=user_id,
        is_completed=False
    )

    # Mock the select query result
    mock_query_result = Mock()
    mock_query_result.first.return_value = mock_task
    mock_db_session.exec.return_value = mock_query_result

    # Act
    result = TaskService.get_task_by_id(task_id, user_id, mock_db_session)

    # Assert
    assert result is not None
    assert result.id == task_id
    assert result.user_id == user_id


def test_get_task_by_id_not_found():
    """Test that getting a non-existent task raises an exception."""
    # Arrange
    task_id = 999  # Non-existent task ID
    user_id = 1
    mock_db_session = Mock(spec=Session)

    # Mock the select query result to return None
    mock_query_result = Mock()
    mock_query_result.first.return_value = None
    mock_db_session.exec.return_value = mock_query_result

    # Act & Assert
    with pytest.raises(Exception):  # Should raise HTTPException
        TaskService.get_task_by_id(task_id, user_id, mock_db_session)


def test_get_tasks_by_user():
    """Test retrieval of all tasks for a user."""
    # Arrange
    user_id = 1
    mock_db_session = Mock(spec=Session)

    mock_tasks = [
        Task(id=1, title="Task 1", user_id=user_id, is_completed=False),
        Task(id=2, title="Task 2", user_id=user_id, is_completed=True)
    ]

    # Mock the select query result
    mock_query_result = Mock()
    mock_query_result.all.return_value = mock_tasks
    mock_db_session.exec.return_value = mock_query_result

    # Act
    result = TaskService.get_tasks_by_user(user_id, mock_db_session)

    # Assert
    assert len(result) == 2
    assert all(task.user_id == user_id for task in result)


def test_get_tasks_by_user_with_filter():
    """Test retrieval of tasks for a user with completion filter."""
    # Arrange
    user_id = 1
    mock_db_session = Mock(spec=Session)

    mock_tasks = [
        Task(id=1, title="Task 1", user_id=user_id, is_completed=True),
        Task(id=2, title="Task 2", user_id=user_id, is_completed=True)
    ]

    # Mock the select query result
    mock_query_result = Mock()
    mock_query_result.all.return_value = mock_tasks
    mock_db_session.exec.return_value = mock_query_result

    # Act
    result = TaskService.get_tasks_by_user(user_id, mock_db_session, completed=True)

    # Assert
    assert len(result) == 2
    assert all(task.is_completed == True for task in result)


def test_update_task_success():
    """Test successful task update."""
    # Arrange
    task_id = 1
    user_id = 1
    task_update = TaskUpdate(title="Updated Title")

    mock_db_session = Mock(spec=Session)

    existing_task = Task(
        id=task_id,
        title="Original Title",
        description="Original Description",
        user_id=user_id,
        is_completed=False
    )

    # Mock the select query result
    mock_query_result = Mock()
    mock_query_result.first.return_value = existing_task
    mock_db_session.exec.return_value = mock_query_result

    mock_db_session.add = Mock()
    mock_db_session.commit = Mock()
    mock_db_session.refresh = Mock()

    # Act
    result = TaskService.update_task(task_id, task_update, user_id, mock_db_session)

    # Assert
    assert result is not None
    assert result.title == "Updated Title"
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()


def test_update_task_not_found():
    """Test that updating a non-existent task raises an exception."""
    # Arrange
    task_id = 999  # Non-existent task ID
    user_id = 1
    task_update = TaskUpdate(title="Updated Title")

    mock_db_session = Mock(spec=Session)

    # Mock the select query result to return None
    mock_query_result = Mock()
    mock_query_result.first.return_value = None
    mock_db_session.exec.return_value = mock_query_result

    # Act & Assert
    with pytest.raises(Exception):  # Should raise HTTPException
        TaskService.update_task(task_id, task_update, user_id, mock_db_session)


def test_delete_task_success():
    """Test successful task deletion."""
    # Arrange
    task_id = 1
    user_id = 1
    mock_db_session = Mock(spec=Session)

    existing_task = Task(
        id=task_id,
        title="Task to Delete",
        user_id=user_id,
        is_completed=False
    )

    # Mock the select query result
    mock_query_result = Mock()
    mock_query_result.first.return_value = existing_task
    mock_db_session.exec.return_value = mock_query_result

    mock_db_session.delete = Mock()
    mock_db_session.commit = Mock()

    # Act
    result = TaskService.delete_task(task_id, user_id, mock_db_session)

    # Assert
    assert result is True
    mock_db_session.delete.assert_called_once_with(existing_task)
    mock_db_session.commit.assert_called_once()


def test_delete_task_not_found():
    """Test that deleting a non-existent task raises an exception."""
    # Arrange
    task_id = 999  # Non-existent task ID
    user_id = 1
    mock_db_session = Mock(spec=Session)

    # Mock the select query result to return None
    mock_query_result = Mock()
    mock_query_result.first.return_value = None
    mock_db_session.exec.return_value = mock_query_result

    # Act & Assert
    with pytest.raises(Exception):  # Should raise HTTPException
        TaskService.delete_task(task_id, user_id, mock_db_session)


def test_get_user_task_count():
    """Test getting the count of tasks for a user."""
    # Arrange
    user_id = 1
    mock_db_session = Mock(spec=Session)

    mock_tasks = [
        Task(id=1, title="Task 1", user_id=user_id, is_completed=False),
        Task(id=2, title="Task 2", user_id=user_id, is_completed=True)
    ]

    # Mock the select query result
    mock_query_result = Mock()
    mock_query_result.all.return_value = mock_tasks
    mock_db_session.exec.return_value = mock_query_result

    # Act
    result = TaskService.get_user_task_count(user_id, mock_db_session)

    # Assert
    assert result == 2


def test_get_user_completed_tasks_count():
    """Test getting the count of completed tasks for a user."""
    # Arrange
    user_id = 1
    mock_db_session = Mock(spec=Session)

    mock_tasks = [
        Task(id=1, title="Task 1", user_id=user_id, is_completed=True),
        Task(id=2, title="Task 2", user_id=user_id, is_completed=True),
        Task(id=3, title="Task 3", user_id=user_id, is_completed=False)
    ]

    # Mock the select query result
    mock_query_result = Mock()
    mock_query_result.all.return_value = mock_tasks
    mock_db_session.exec.return_value = mock_query_result

    # Act
    result = TaskService.get_user_completed_tasks_count(user_id, mock_db_session)

    # Assert - counting only completed tasks (2 out of 3)
    assert result == 2