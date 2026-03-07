"""
Official MCP Server Implementation for TaskFlow Todo App.

This module implements the Model Context Protocol (MCP) server
using the official MCP SDK to expose task management tools.
"""

from __future__ import annotations

import asyncio
import json
import os
from typing import Any, Dict, List, Optional
from contextlib import asynccontextmanager

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    Resource,
    ResourceTemplate,
)
from sqlmodel import Session, create_engine, select

from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.user import User
from ..database import get_session


# Create MCP server instance
mcp_server = Server("taskflow-todo-server")


def _status_to_completed(status: Optional[str]) -> Optional[bool]:
    """Convert status string to boolean for filtering."""
    if status is None or status == "all":
        return None
    if status == "completed":
        return True
    if status == "pending":
        return False
    return None


@mcp_server.list_tools()
async def list_tools() -> List[Tool]:
    """List all available MCP tools."""
    return [
        Tool(
            name="add_task",
            description="Create a new task for the user. Returns task ID and confirmation.",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The ID of the user who owns the task"
                    },
                    "title": {
                        "type": "string",
                        "description": "Task title (required, 1-200 characters)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional task description (max 1000 characters)"
                    },
                },
                "required": ["user_id", "title"],
            },
        ),
        Tool(
            name="list_tasks",
            description="List tasks for the user, optionally filtered by status.",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The ID of the user"
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by status: all, pending, completed",
                        "enum": ["all", "pending", "completed"],
                    },
                },
                "required": ["user_id"],
            },
        ),
        Tool(
            name="complete_task",
            description="Mark a task as completed.",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The ID of the user"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to complete"
                    },
                },
                "required": ["user_id", "task_id"],
            },
        ),
        Tool(
            name="update_task",
            description="Update a task's title or description.",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The ID of the user"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New task title"
                    },
                    "description": {
                        "type": "string",
                        "description": "New task description"
                    },
                },
                "required": ["user_id", "task_id"],
            },
        ),
        Tool(
            name="delete_task",
            description="Delete a task permanently.",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The ID of the user"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to delete"
                    },
                },
                "required": ["user_id", "task_id"],
            },
        ),
    ]


@mcp_server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls from the AI agent."""
    try:
        # Get database session
        # Note: In production, you'd want to manage sessions more carefully
        from ..database import engine
        with Session(engine) as session:
            if name == "add_task":
                result = await _add_task(arguments, session)
            elif name == "list_tasks":
                result = await _list_tasks(arguments, session)
            elif name == "complete_task":
                result = await _complete_task(arguments, session)
            elif name == "update_task":
                result = await _update_task(arguments, session)
            elif name == "delete_task":
                result = await _delete_task(arguments, session)
            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2))]


async def _add_task(arguments: Dict[str, Any], session: Session) -> Dict[str, Any]:
    """Add a new task."""
    user_id = int(arguments.get("user_id"))
    title = str(arguments.get("title", "")).strip()
    description = arguments.get("description")

    if not title:
        return {"success": False, "error": "Title is required"}

    # Validate user exists
    user = session.get(User, user_id)
    if not user:
        return {"success": False, "error": "User not found"}

    # Create task
    task = Task(
        user_id=user_id,
        title=title,
        description=description if description else None,
    )
    session.add(task)
    session.commit()
    session.refresh(task)

    return {
        "success": True,
        "task_id": task.id,
        "title": task.title,
        "status": "created"
    }


async def _list_tasks(arguments: Dict[str, Any], session: Session) -> Dict[str, Any]:
    """List tasks for a user."""
    user_id = int(arguments.get("user_id"))
    status_filter = arguments.get("status", "all")

    # Validate user exists
    user = session.get(User, user_id)
    if not user:
        return {"success": False, "error": "User not found"}

    # Build query
    statement = select(Task).where(Task.user_id == user_id)

    completed_filter = _status_to_completed(status_filter)
    if completed_filter is not None:
        statement = statement.where(Task.is_completed == completed_filter)

    statement = statement.order_by(Task.created_at.desc())
    tasks = session.exec(statement).all()

    return {
        "success": True,
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.is_completed,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
            }
            for task in tasks
        ],
        "count": len(tasks)
    }


async def _complete_task(arguments: Dict[str, Any], session: Session) -> Dict[str, Any]:
    """Mark a task as completed."""
    user_id = int(arguments.get("user_id"))
    task_id = int(arguments.get("task_id"))

    # Validate user exists
    user = session.get(User, user_id)
    if not user:
        return {"success": False, "error": "User not found"}

    # Get task
    task = session.get(Task, task_id)
    if not task:
        return {"success": False, "error": "Task not found"}

    # Validate ownership
    if task.user_id != user_id:
        return {"success": False, "error": "Task does not belong to user"}

    # Mark as completed
    task.is_completed = True
    session.add(task)
    session.commit()
    session.refresh(task)

    return {
        "success": True,
        "task_id": task.id,
        "title": task.title,
        "status": "completed"
    }


async def _update_task(arguments: Dict[str, Any], session: Session) -> Dict[str, Any]:
    """Update a task."""
    user_id = int(arguments.get("user_id"))
    task_id = int(arguments.get("task_id"))
    title = arguments.get("title")
    description = arguments.get("description")

    # Validate user exists
    user = session.get(User, user_id)
    if not user:
        return {"success": False, "error": "User not found"}

    # Get task
    task = session.get(Task, task_id)
    if not task:
        return {"success": False, "error": "Task not found"}

    # Validate ownership
    if task.user_id != user_id:
        return {"success": False, "error": "Task does not belong to user"}

    # Update fields
    updated_fields = []
    if title is not None:
        task.title = str(title).strip()
        updated_fields.append("title")
    if description is not None:
        task.description = description if description else None
        updated_fields.append("description")

    if not updated_fields:
        return {"success": False, "error": "No fields to update"}

    session.add(task)
    session.commit()
    session.refresh(task)

    return {
        "success": True,
        "task_id": task.id,
        "title": task.title,
        "updated_fields": updated_fields,
        "status": "updated"
    }


async def _delete_task(arguments: Dict[str, Any], session: Session) -> Dict[str, Any]:
    """Delete a task."""
    user_id = int(arguments.get("user_id"))
    task_id = int(arguments.get("task_id"))

    # Validate user exists
    user = session.get(User, user_id)
    if not user:
        return {"success": False, "error": "User not found"}

    # Get task
    task = session.get(Task, task_id)
    if not task:
        return {"success": False, "error": "Task not found"}

    # Validate ownership
    if task.user_id != user_id:
        return {"success": False, "error": "Task does not belong to user"}

    # Store title for response
    task_title = task.title

    # Delete task
    session.delete(task)
    session.commit()

    return {
        "success": True,
        "task_id": task_id,
        "title": task_title,
        "status": "deleted"
    }


# Export tool definitions for use in chat service
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "User ID"},
                    "title": {"type": "string", "description": "Task title"},
                    "description": {"type": "string", "description": "Task description"},
                },
                "required": ["user_id", "title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List tasks for the user, optionally filtered by status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "User ID"},
                    "status": {
                        "type": "string",
                        "description": "Filter by status: all, pending, completed",
                        "enum": ["all", "pending", "completed"],
                    },
                },
                "required": ["user_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "User ID"},
                    "task_id": {"type": "integer", "description": "Task ID"},
                },
                "required": ["user_id", "task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update a task title or description.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "User ID"},
                    "task_id": {"type": "integer", "description": "Task ID"},
                    "title": {"type": "string", "description": "New task title"},
                    "description": {"type": "string", "description": "New task description"},
                },
                "required": ["user_id", "task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "User ID"},
                    "task_id": {"type": "integer", "description": "Task ID"},
                },
                "required": ["user_id", "task_id"],
            },
        },
    },
]


# For standalone MCP server mode (optional)
async def run_mcp_server():
    """Run the MCP server in standalone mode."""
    from ..database import engine
    
    async with stdio_server() as (read_stream, write_stream):
        await mcp_server.run(
            read_stream,
            write_stream,
            mcp_server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(run_mcp_server())
