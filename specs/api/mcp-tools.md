# MCP Tools Specification

## Overview
The MCP (Model Context Protocol) server exposes task operations as tools for the AI agent.

## Tool Definitions

### Tool: add_task
**Purpose:** Create a new task for the user.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | integer | Yes | The ID of the user |
| title | string | Yes | Task title (1-200 characters) |
| description | string | No | Optional task description |

**Returns:**
```json
{
  "task_id": 123,
  "status": "created",
  "title": "Buy groceries"
}
```

**Example Input:**
```json
{
  "user_id": 1,
  "title": "Buy groceries",
  "description": "Milk and eggs"
}
```

---

### Tool: list_tasks
**Purpose:** List tasks for the user, optionally filtered by status.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | integer | Yes | The ID of the user |
| status | string | No | Filter: "all", "pending", "completed" (default: "all") |

**Returns:**
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk and eggs",
    "completed": false,
    "created_at": "2025-12-01T10:00:00Z",
    "updated_at": "2025-12-01T10:00:00Z"
  }
]
```

**Example Input:**
```json
{
  "user_id": 1,
  "status": "pending"
}
```

---

### Tool: complete_task
**Purpose:** Mark a task as completed.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | integer | Yes | The ID of the user |
| task_id | integer | Yes | The ID of the task to complete |

**Returns:**
```json
{
  "task_id": 1,
  "status": "completed",
  "title": "Buy groceries"
}
```

**Example Input:**
```json
{
  "user_id": 1,
  "task_id": 1
}
```

---

### Tool: update_task
**Purpose:** Update a task's title or description.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | integer | Yes | The ID of the user |
| task_id | integer | Yes | The ID of the task to update |
| title | string | No | New task title |
| description | string | No | New task description |

**Returns:**
```json
{
  "task_id": 1,
  "status": "updated",
  "title": "Buy groceries and cook dinner"
}
```

**Example Input:**
```json
{
  "user_id": 1,
  "task_id": 1,
  "title": "Buy groceries and cook dinner"
}
```

---

### Tool: delete_task
**Purpose:** Delete a task.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | integer | Yes | The ID of the user |
| task_id | integer | Yes | The ID of the task to delete |

**Returns:**
```json
{
  "task_id": 1,
  "status": "deleted"
}
```

**Example Input:**
```json
{
  "user_id": 1,
  "task_id": 1
}
```

---

## Error Handling

All tools return errors in a consistent format:

```json
{
  "success": false,
  "error": "Task not found"
}
```

### Common Errors
| Error | HTTP Code | Description |
|-------|-----------|-------------|
| Task not found | 404 | Task ID doesn't exist or doesn't belong to user |
| Invalid user_id | 401 | User ID doesn't match authenticated user |
| Invalid input | 400 | Missing required fields or invalid data |

## Implementation Status
✅ Complete - See `backend/src/mcp_server/tools.py`
