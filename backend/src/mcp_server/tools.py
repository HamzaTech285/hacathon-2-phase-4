"""MCP tool implementations using Official MCP SDK."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from fastapi import HTTPException
from sqlmodel import Session

# Re-export from official MCP server implementation
from .server import TOOL_DEFINITIONS

# Import tool execution functions
from ..models.task import TaskCreate, TaskUpdate
from ..services.task_service import TaskService


def _status_to_completed(status: Optional[str]) -> Optional[bool]:
    """Convert status string to boolean for filtering."""
    if status is None or status == "all":
        return None
    if status == "completed":
        return True
    if status == "pending":
        return False
    return None


def _normalize_user_id(args: Dict[str, Any], user_id: int) -> int:
    """Normalize user ID from arguments or context."""
    return int(args.get("user_id", user_id))


async def run_tool(tool_name: str, args: Dict[str, Any], session: Session, user_id: int) -> Dict[str, Any] | List[Dict[str, Any]]:
    """
    Dispatch MCP tool calls to task operations.
    
    This function is compatible with both:
    - Official MCP SDK tool execution
    - OpenAI function calling format
    
    Args:
        tool_name: Name of the tool to execute
        args: Tool arguments
        session: Database session
        user_id: Authenticated user ID
        
    Returns:
        Tool execution result
    """
    normalized_user_id = _normalize_user_id(args, user_id)

    if tool_name == "add_task":
        task_data = TaskCreate(
            title=args["title"],
            description=args.get("description"),
            user_id=normalized_user_id,
        )
        task = TaskService.create_task(task_data, session)
        return {"task_id": task.id, "status": "created", "title": task.title}

    if tool_name == "list_tasks":
        completed_filter = _status_to_completed(args.get("status"))
        tasks = TaskService.get_tasks_by_user(normalized_user_id, session, completed=completed_filter)
        return [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.is_completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
            }
            for task in tasks
        ]

    if tool_name == "complete_task":
        task_id = int(args["task_id"])
        task = TaskService.update_task(task_id, TaskUpdate(is_completed=True), normalized_user_id, session)
        return {"task_id": task.id, "status": "completed", "title": task.title}

    if tool_name == "delete_task":
        task_id = int(args["task_id"])
        TaskService.delete_task(task_id, normalized_user_id, session)
        return {"task_id": task_id, "status": "deleted"}

    if tool_name == "update_task":
        task_id = int(args["task_id"])
        update = TaskUpdate(
            title=args.get("title"),
            description=args.get("description"),
        )
        task = TaskService.update_task(task_id, update, normalized_user_id, session)
        return {"task_id": task.id, "status": "updated", "title": task.title}

    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool_name}")
