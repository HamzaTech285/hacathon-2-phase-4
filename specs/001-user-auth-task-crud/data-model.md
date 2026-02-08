# Data Model: Full-Stack Todo App with Authentication

## Entity: User

### Fields
- `id` (UUID/Integer): Primary key, unique identifier for the user
- `email` (String): User's email address, required, unique
- `password_hash` (String): Hashed password, managed by Better Auth
- `created_at` (DateTime): Timestamp when user was created
- `updated_at` (DateTime): Timestamp when user was last updated
- `is_active` (Boolean): Whether the user account is active

### Relationships
- `tasks`: One-to-many relationship with Task entity (one user can have many tasks)

### Validation Rules
- Email must be valid format
- Email must be unique across all users
- Password must meet security requirements (handled by Better Auth)

## Entity: Task

### Fields
- `id` (UUID/Integer): Primary key, unique identifier for the task
- `title` (String): Task title, required, max length 255
- `description` (Text): Optional task description
- `is_completed` (Boolean): Whether the task is completed, default false
- `user_id` (UUID/Integer): Foreign key linking to User, required
- `created_at` (DateTime): Timestamp when task was created
- `updated_at` (DateTime): Timestamp when task was last updated
- `due_date` (DateTime, optional): Optional deadline for the task

### Relationships
- `user`: Many-to-one relationship with User entity (many tasks belong to one user)

### Validation Rules
- Title is required and cannot exceed 255 characters
- Description is optional and has reasonable length limits
- user_id must reference an existing user
- Only the task owner can modify the task

## State Transitions

### Task States
- `pending` (is_completed=False): Task is created but not yet completed
- `completed` (is_completed=True): Task has been marked as completed

### Valid State Transitions
- `pending` → `completed`: When user marks task as done
- `completed` → `pending`: When user unmarks task as done

## Database Constraints

### Primary Keys
- Both User and Task tables have auto-incrementing integer primary keys

### Foreign Keys
- Task.user_id references User.id with cascade delete (deleting a user deletes their tasks)

### Unique Constraints
- User.email must be unique

### Indexes
- Index on User.email for fast lookup
- Index on Task.user_id for efficient filtering by user
- Index on Task.is_completed for filtering completed tasks

## SQLModel Implementation

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
import uuid
from datetime import datetime

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")

class TaskBase(SQLModel):
    title: str = Field(max_length=255)
    description: Optional[str] = None
    is_completed: bool = False
    user_id: int = Field(foreign_key="user.id")
    due_date: Optional[datetime] = None

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: User = Relationship(back_populates="tasks")
```