"""Chat service for AI-powered task management."""

import json
import os
from typing import Optional

from openai import OpenAI
from sqlmodel import Session, select

from ..models.conversation import Conversation, Message
from ..models.task import Task
from ..mcp_server.tools import TOOL_DEFINITIONS, run_tool


class ChatService:
    """Service for handling chat interactions with OpenAI."""

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.system_prompt = """You are a helpful task management assistant for TaskFlow.
You help users manage their todo tasks through natural language conversation.

You can help with:
- Creating new tasks
- Listing tasks
- Marking tasks as complete
- Updating task details
- Deleting tasks

Be friendly, concise, and helpful. When users ask about tasks, provide clear information.
If they want to create a task, ask for necessary details like title and description.
Always confirm actions taken by tools and summarize results for the user.
"""
    
    @staticmethod
    def get_or_create_conversation(session: Session, user_id: int, conversation_id: Optional[int] = None) -> Conversation:
        """Get existing conversation or create a new one."""
        if conversation_id:
            conversation = session.get(Conversation, conversation_id)
            if conversation and conversation.user_id == user_id:
                return conversation
        
        # Create new conversation
        conversation = Conversation(user_id=user_id, title="New Chat")
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation
    
    @staticmethod
    def get_conversation_history(session: Session, conversation_id: int, limit: int = 10) -> list[dict]:
        """Get recent messages from a conversation."""
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        messages = session.exec(statement).all()
        
        # Reverse to get chronological order
        return [
            {"role": msg.role, "content": msg.content}
            for msg in reversed(messages)
        ]
    
    @staticmethod
    def save_message(session: Session, conversation_id: int, role: str, content: str, tool_calls: Optional[dict] = None) -> Message:
        """Save a message to the database."""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            tool_calls=tool_calls
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message
    
    async def generate_response(self, session: Session, user_id: int, user_message: str, conversation_id: Optional[int] = None) -> dict:
        """Generate AI response for user message."""

        # Get or create conversation
        conversation = self.get_or_create_conversation(session, user_id, conversation_id)

        # Save user message
        self.save_message(session, conversation.id, "user", user_message)

        # Get conversation history
        history = self.get_conversation_history(session, conversation.id)

        # Build messages for OpenAI
        messages = [
            {"role": "system", "content": self.system_prompt},
            *history,
            {"role": "user", "content": user_message},
        ]

        # Get task context for better responses
        task_context = self._get_task_context(session, user_id)
        if task_context:
            messages[0]["content"] += f"\n\nUser's current tasks:\n{task_context}"

        # Call OpenAI API with MCP tool definitions
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.2,
                max_tokens=500,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto",
            )

            assistant_message = response.choices[0].message
            tool_calls = assistant_message.tool_calls or []

            # Execute tool calls (MCP tools)
            tool_results = []
            if tool_calls:
                for tool_call in tool_calls:
                    tool_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments or "{}")
                    result = await run_tool(tool_name, args, session, user_id)
                    tool_results.append({
                        "tool": tool_name,
                        "arguments": args,
                        "result": result,
                    })

                # Add tool results to messages for final response
                messages.append({
                    "role": "assistant",
                    "tool_calls": tool_calls,
                    "content": assistant_message.content or "",
                })

                for tool_call, result in zip(tool_calls, tool_results):
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result["result"]),
                    })

                follow_up = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    temperature=0.2,
                    max_tokens=500,
                )
                final_message = follow_up.choices[0].message.content
            else:
                final_message = assistant_message.content or ""

            # Save assistant message
            self.save_message(
                session,
                conversation.id,
                "assistant",
                final_message,
                tool_calls=tool_results or None,
            )

            return {
                "conversation_id": conversation.id,
                "response": final_message,
                "tool_calls": tool_results,
            }

        except Exception as e:
            error_message = f"I encountered an error: {str(e)}"
            self.save_message(session, conversation.id, "assistant", error_message)
            return {
                "conversation_id": conversation.id,
                "response": error_message,
                "tool_calls": [],
            }
    
    @staticmethod
    def _get_task_context(session: Session, user_id: int) -> str:
        """Get user's tasks for context."""
        statement = select(Task).where(Task.user_id == user_id).limit(10)
        tasks = session.exec(statement).all()
        
        if not tasks:
            return "No tasks yet."
        
        task_list = []
        for task in tasks:
            status = "✅" if task.is_completed else "⏳"
            task_list.append(f"{status} {task.title}")
        
        return "\n".join(task_list)
