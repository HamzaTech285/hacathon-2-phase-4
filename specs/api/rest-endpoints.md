# REST API Endpoints Specification

## Base URL
- Development: http://localhost:8000
- Production: https://api.example.com

## Authentication
All endpoints (except health check) require JWT token in header:
```
Authorization: Bearer <token>
```

---

## Authentication Endpoints

### POST /api/auth/signup
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "user"
  }
}
```

### POST /api/auth/login
Authenticate existing user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

---

## Task Endpoints

### GET /api/tasks
List all tasks for authenticated user.

**Query Parameters:**
- `completed` (optional): Filter by completion status
  - `true` - Only completed tasks
  - `false` - Only pending tasks
  - omitted - All tasks

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "is_completed": false,
    "due_date": null,
    "created_at": "2025-12-01T10:00:00Z",
    "updated_at": "2025-12-01T10:00:00Z"
  }
]
```

### POST /api/tasks
Create a new task.

**Request Body:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "due_date": "2025-12-15T18:00:00Z"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_completed": false,
  "due_date": "2025-12-15T18:00:00Z",
  "created_at": "2025-12-01T10:00:00Z",
  "updated_at": "2025-12-01T10:00:00Z"
}
```

### GET /api/tasks/{task_id}
Get specific task details.

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_completed": false,
  "due_date": "2025-12-15T18:00:00Z",
  "created_at": "2025-12-01T10:00:00Z",
  "updated_at": "2025-12-01T10:00:00Z"
}
```

### PUT /api/tasks/{task_id}
Update a task.

**Request Body:**
```json
{
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken",
  "is_completed": true,
  "due_date": "2025-12-15T20:00:00Z"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken",
  "is_completed": true,
  "due_date": "2025-12-15T20:00:00Z",
  "created_at": "2025-12-01T10:00:00Z",
  "updated_at": "2025-12-01T12:00:00Z"
}
```

### DELETE /api/tasks/{task_id}
Delete a task.

**Response (200 OK):**
```json
{
  "message": "Task deleted successfully"
}
```

---

## Chat Endpoints

### POST /api/chat
Send message to AI assistant and get response.

**Request Body:**
```json
{
  "conversation_id": 456,
  "message": "Add a task to buy groceries tomorrow"
}
```

**Response (200 OK):**
```json
{
  "conversation_id": 456,
  "response": "I've added a task for you: 'Buy groceries tomorrow'. Task ID is 789.",
  "tool_calls": [
    {
      "tool": "add_task",
      "arguments": {
        "user_id": 1,
        "title": "Buy groceries tomorrow",
        "description": null
      },
      "result": {
        "success": true,
        "task_id": 789,
        "title": "Buy groceries tomorrow"
      }
    }
  ]
}
```

---

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 404 Not Found
```json
{
  "detail": "Task not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "An error occurred"
}
```
