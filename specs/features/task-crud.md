# Feature: Task CRUD Operations

## User Stories
- As a user, I can create a new task
- As a user, I can view all my tasks
- As a user, I can update a task
- As a user, I can delete a task
- As a user, I can mark a task complete

## Acceptance Criteria

### Create Task
- Title is required (1-200 characters)
- Description is optional (max 1000 characters)
- Task is associated with logged-in user
- Returns created task with ID and timestamps

### View Tasks
- Only show tasks for current user
- Display title, description, status, created date
- Support filtering by status (all, pending, completed)
- Support pagination (optional)

### Update Task
- Can update title, description, and completion status
- Must validate task ownership (user can only update their own tasks)
- Returns updated task with new timestamps

### Delete Task
- Can delete task by ID
- Must validate task ownership
- Returns success message
- Task is permanently removed from database

### Mark Complete
- Can toggle task completion status
- Must validate task ownership
- Returns updated task

## API Endpoints
- `GET /api/tasks` - List all tasks for authenticated user
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get task details
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task

## Implementation Status
✅ Complete - See `backend/src/api/task_router.py`
