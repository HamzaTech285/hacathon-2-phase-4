from __future__ import annotations
"""Task API router with CRUD endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from ..database import get_session
from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
from ..services.task_service import TaskService
from ..auth_handler import get_current_user


task_router = APIRouter(prefix="/tasks", tags=["tasks"])


@task_router.get("/", response_model=List[TaskRead])
def get_tasks(
    completed: bool = None,
    db_session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """
    Get all tasks for the authenticated user.

    Args:
        completed: Optional filter for completed/incomplete tasks
        db_session: Database session for database operations
        current_user: The currently authenticated user (from JWT token)

    Returns:
        List[TaskRead]: List of tasks belonging to the user
    """
    try:
        user_id = current_user.get("user_id")
        tasks = TaskService.get_tasks_by_user(user_id, db_session, completed)
        return tasks
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving tasks: {str(e)}"
        )


@task_router.post("/", response_model=TaskRead)
def create_task(
    task_data: TaskCreate,
    db_session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new task for the authenticated user.

    Args:
        task_data: Task creation data
        db_session: Database session for database operations
        current_user: The currently authenticated user (from JWT token)

    Returns:
        TaskRead: The created task
    """
    try:
        user_id = current_user.get("user_id")

        # Override user_id to ensure user can only create tasks for themselves
        task_data.user_id = user_id

        task = TaskService.create_task(task_data, db_session)
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the task: {str(e)}"
        )


@task_router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    db_session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific task by ID for the authenticated user.

    Args:
        task_id: The ID of the task to retrieve
        db_session: Database session for database operations
        current_user: The currently authenticated user (from JWT token)

    Returns:
        TaskRead: The requested task
    """
    try:
        user_id = current_user.get("user_id")
        task = TaskService.get_task_by_id(task_id, user_id, db_session)
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving the task: {str(e)}"
        )


@task_router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db_session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """
    Update a specific task by ID for the authenticated user.

    Args:
        task_id: The ID of the task to update
        task_update: Task update data
        db_session: Database session for database operations
        current_user: The currently authenticated user (from JWT token)

    Returns:
        TaskRead: The updated task
    """
    try:
        user_id = current_user.get("user_id")
        updated_task = TaskService.update_task(task_id, task_update, user_id, db_session)
        return updated_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the task: {str(e)}"
        )


@task_router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db_session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a specific task by ID for the authenticated user.

    Args:
        task_id: The ID of the task to delete
        db_session: Database session for database operations
        current_user: The currently authenticated user (from JWT token)

    Returns:
        dict: Success message
    """
    try:
        user_id = current_user.get("user_id")
        success = TaskService.delete_task(task_id, user_id, db_session)
        if success:
            return {"message": "Task deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the task: {str(e)}"
        )