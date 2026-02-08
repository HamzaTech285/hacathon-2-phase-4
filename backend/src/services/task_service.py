"""Task service for CRUD operations on tasks."""

from sqlmodel import Session, select
from typing import List, Optional
from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
from ..models.user import User
from fastapi import HTTPException, status


class TaskService:
    """Service class for task operations."""

    @staticmethod
    def create_task(task_data: TaskCreate, db_session: Session) -> Task:
        """
        Create a new task.

        Args:
            task_data: Task creation data
            db_session: Database session for database operations

        Returns:
            Task: The created task object
        """
        # Verify the user exists
        user = db_session.get(User, task_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Create new task
        db_task = Task.from_orm(task_data) if hasattr(Task, 'from_orm') else Task(**task_data.dict())

        # For SQLModel, we need to manually assign the attributes
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            is_completed=task_data.is_completed,
            user_id=task_data.user_id,
            due_date=task_data.due_date
        )

        # Add to database
        db_session.add(db_task)
        db_session.commit()
        db_session.refresh(db_task)

        return db_task

    @staticmethod
    def get_task_by_id(task_id: int, user_id: int, db_session: Session) -> Optional[Task]:
        """
        Get a task by its ID for a specific user.

        Args:
            task_id: The ID of the task to retrieve
            user_id: The ID of the user requesting the task
            db_session: Database session for database operations

        Returns:
            Task: The task object if found and belongs to the user, None otherwise
        """
        task = db_session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        return task

    @staticmethod
    def get_tasks_by_user(user_id: int, db_session: Session, completed: Optional[bool] = None) -> List[Task]:
        """
        Get all tasks for a specific user.

        Args:
            user_id: The ID of the user whose tasks to retrieve
            db_session: Database session for database operations
            completed: Optional filter for completed/incomplete tasks

        Returns:
            List[Task]: List of tasks belonging to the user
        """
        query = select(Task).where(Task.user_id == user_id)

        if completed is not None:
            query = query.where(Task.is_completed == completed)

        tasks = db_session.exec(query).all()
        return tasks

    @staticmethod
    def update_task(task_id: int, task_update: TaskUpdate, user_id: int, db_session: Session) -> Optional[Task]:
        """
        Update a task for a specific user.

        Args:
            task_id: The ID of the task to update
            task_update: Task update data
            user_id: The ID of the user requesting the update
            db_session: Database session for database operations

        Returns:
            Task: The updated task object if successful, None otherwise
        """
        # Get the existing task
        task = db_session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Update the task with provided values
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        # Update the updated_at timestamp
        from datetime import datetime
        task.updated_at = datetime.utcnow()

        # Commit changes
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        return task

    @staticmethod
    def delete_task(task_id: int, user_id: int, db_session: Session) -> bool:
        """
        Delete a task for a specific user.

        Args:
            task_id: The ID of the task to delete
            user_id: The ID of the user requesting the deletion
            db_session: Database session for database operations

        Returns:
            bool: True if the task was deleted, False otherwise
        """
        # Get the existing task
        task = db_session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Delete the task
        db_session.delete(task)
        db_session.commit()

        return True

    @staticmethod
    def get_user_task_count(user_id: int, db_session: Session) -> int:
        """
        Get the total count of tasks for a specific user.

        Args:
            user_id: The ID of the user whose task count to retrieve
            db_session: Database session for database operations

        Returns:
            int: The number of tasks belonging to the user
        """
        query = select(Task).where(Task.user_id == user_id)
        tasks = db_session.exec(query).all()
        return len(tasks)

    @staticmethod
    def get_user_completed_tasks_count(user_id: int, db_session: Session) -> int:
        """
        Get the count of completed tasks for a specific user.

        Args:
            user_id: The ID of the user whose completed task count to retrieve
            db_session: Database session for database operations

        Returns:
            int: The number of completed tasks belonging to the user
        """
        query = select(Task).where(Task.user_id == user_id, Task.is_completed == True)
        completed_tasks = db_session.exec(query).all()
        return len(completed_tasks)