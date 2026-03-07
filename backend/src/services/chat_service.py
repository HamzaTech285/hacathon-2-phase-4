"""Chat service for AI-powered task management using OpenAI Agents SDK and OpenRouter API."""

import json
import os
from typing import Optional

from sqlmodel import Session, select

from ..models.conversation import Conversation, Message
from ..models.task import Task
from ..mcp_server.tools import TOOL_DEFINITIONS, run_tool
from ..agents.taskflow_agent import TaskFlowAgent, AgentConfig


class ChatService:
    """Service for handling chat interactions using OpenAI Agents SDK with OpenRouter API."""

    def __init__(self):
        # Initialize TaskFlow Agent with OpenRouter configuration
        self.agent = TaskFlowAgent(
            config=AgentConfig(
                model="openai/gpt-4o-mini",
                temperature=0.2,
                max_tokens=500,
            )
        )
        # Set MCP tools for the agent
        self.agent.set_tools(TOOL_DEFINITIONS)
    
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
        """Generate AI response for user message using OpenAI Agents SDK."""

        # Get or create conversation
        conversation = self.get_or_create_conversation(session, user_id, conversation_id)

        # Save user message
        self.save_message(session, conversation.id, "user", user_message)

        # Get conversation history
        history = self.get_conversation_history(session, conversation.id)

        # Get task context for better responses
        task_context = self._get_task_context(session, user_id)

        # Run the agent with conversation history and task context
        try:
            agent_response = await self.agent.run(
                messages=[
                    {"role": "system", "content": self.agent.config.system_prompt},
                    *history,
                    {"role": "user", "content": user_message},
                ],
                tool_handler=lambda tool_name, args: run_tool(tool_name, args, session, user_id),
            )

            # Save assistant message with tool calls
            self.save_message(
                session,
                conversation.id,
                "assistant",
                agent_response.content,
                tool_calls=agent_response.tool_calls or None,
            )

            return {
                "conversation_id": conversation.id,
                "response": agent_response.content,
                "tool_calls": agent_response.tool_calls,
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
