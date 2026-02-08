# API Contract: Full-Stack Todo App with Authentication

## Authentication API

### POST /auth/signup
Register a new user account.

**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "token": "jwt_token_string"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Invalid email format or password too weak"
}
```

**Response (409 Conflict):**
```json
{
  "error": "Email already registered"
}
```

### POST /auth/login
Authenticate a user and return JWT token.

**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "token": "jwt_token_string"
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Invalid credentials"
}
```

## Task Management API

All task endpoints require a valid JWT token in the Authorization header:

`Authorization: Bearer <jwt_token>`

### GET /tasks
Retrieve all tasks for the authenticated user.

**Headers:**
- `Authorization: Bearer <jwt_token>`

**Response (200 OK):**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Sample task",
      "description": "Sample description",
      "is_completed": false,
      "user_id": 1,
      "created_at": "2026-02-02T10:00:00Z",
      "updated_at": "2026-02-02T10:00:00Z",
      "due_date": null
    }
  ]
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Unauthorized access - invalid or missing token"
}
```

### POST /tasks
Create a new task for the authenticated user.

**Headers:**
- `Authorization: Bearer <jwt_token>`

**Request Body:**
```json
{
  "title": "New task",
  "description": "Task description",
  "is_completed": false,
  "due_date": "2026-12-31T23:59:59Z"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "New task",
  "description": "Task description",
  "is_completed": false,
  "user_id": 1,
  "created_at": "2026-02-02T10:00:00Z",
  "updated_at": "2026-02-02T10:00:00Z",
  "due_date": "2026-12-31T23:59:59Z"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Validation error - title is required"
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Unauthorized access - invalid or missing token"
}
```

### PUT /tasks/{id}
Update an existing task for the authenticated user.

**Path Parameters:**
- `id` (integer): Task ID

**Headers:**
- `Authorization: Bearer <jwt_token>`

**Request Body:**
```json
{
  "title": "Updated task",
  "description": "Updated description",
  "is_completed": true,
  "due_date": "2026-12-31T23:59:59Z"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Updated task",
  "description": "Updated description",
  "is_completed": true,
  "user_id": 1,
  "created_at": "2026-02-02T10:00:00Z",
  "updated_at": "2026-02-02T11:00:00Z",
  "due_date": "2026-12-31T23:59:59Z"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Validation error - title is required"
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Unauthorized access - invalid or missing token"
}
```

**Response (403 Forbidden):**
```json
{
  "error": "Access denied - task does not belong to user"
}
```

**Response (404 Not Found):**
```json
{
  "error": "Task not found"
}
```

### DELETE /tasks/{id}
Delete an existing task for the authenticated user.

**Path Parameters:**
- `id` (integer): Task ID

**Headers:**
- `Authorization: Bearer <jwt_token>`

**Response (204 No Content):**
Empty response body

**Response (401 Unauthorized):**
```json
{
  "error": "Unauthorized access - invalid or missing token"
}
```

**Response (403 Forbidden):**
```json
{
  "error": "Access denied - task does not belong to user"
}
```

**Response (404 Not Found):**
```json
{
  "error": "Task not found"
}
```

## Error Response Format

All error responses follow this format:
```json
{
  "error": "Descriptive error message"
}
```

## Security Requirements

1. All task-related endpoints require a valid JWT token in the Authorization header
2. The system validates that the requesting user owns the task before performing operations
3. Invalid or expired tokens result in 401 Unauthorized responses
4. Attempts to access another user's tasks result in 403 Forbidden responses