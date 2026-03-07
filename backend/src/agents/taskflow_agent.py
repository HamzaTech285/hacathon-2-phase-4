"""
OpenAI Agents SDK Integration for TaskFlow.

This module provides integration with the OpenAI Agents SDK
for building AI-powered task management agents.
"""

from __future__ import annotations

import os
import json
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionToolParam


@dataclass
class AgentConfig:
    """Configuration for the TaskFlow AI Agent."""
    model: str = "openai/gpt-4o-mini"
    temperature: float = 0.2
    max_tokens: int = 500
    system_prompt: str = """You are a helpful task management assistant for TaskFlow.
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

Available tools:
- add_task: Create a new task
- list_tasks: List all tasks or filter by status
- complete_task: Mark a task as completed
- update_task: Update task title or description
- delete_task: Delete a task

When using tools, always confirm the action in a friendly way.
"""


class TaskFlowAgent:
    """
    AI Agent for task management using OpenAI Agents SDK patterns.
    
    This agent uses OpenAI's function calling capabilities
    to interact with task management tools.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        config: Optional[AgentConfig] = None
    ):
        """
        Initialize the TaskFlow Agent.
        
        Args:
            api_key: OpenRouter API key (defaults to OPENROUTER_API_KEY env var)
            base_url: API base URL (defaults to OpenRouter)
            config: Agent configuration
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
        
        self.base_url = base_url or "https://openrouter.ai/api/v1"
        self.config = config or AgentConfig()
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        self.tools: List[ChatCompletionToolParam] = []

    def set_tools(self, tools: List[ChatCompletionToolParam]) -> None:
        """Set the tools available to the agent."""
        self.tools = tools

    def prepare_messages(
        self,
        conversation_history: List[Dict[str, str]],
        user_message: str,
        task_context: Optional[str] = None
    ) -> List[ChatCompletionMessageParam]:
        """
        Prepare messages for the agent.
        
        Args:
            conversation_history: Previous messages in conversation
            user_message: Current user message
            task_context: Optional context about user's tasks
            
        Returns:
            Formatted message list for OpenAI API
        """
        system_prompt = self.config.system_prompt
        
        # Add task context if available
        if task_context:
            system_prompt += f"\n\nUser's current tasks:\n{task_context}"
        
        messages: List[ChatCompletionMessageParam] = [
            {"role": "system", "content": system_prompt},
        ]
        
        # Add conversation history (last 10 messages)
        messages.extend(conversation_history[-10:])
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        return messages

    async def run(
        self,
        messages: List[ChatCompletionMessageParam],
        tool_handler: callable = None
    ) -> AgentResponse:
        """
        Run the agent with the given messages.
        
        Args:
            messages: Message history
            tool_handler: Function to handle tool calls
            
        Returns:
            AgentResponse with assistant message and tool calls
        """
        try:
            # Make initial completion
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                tools=self.tools if self.tools else None,
                tool_choice="auto" if self.tools else None,
                extra_headers={
                    "HTTP-Referer": "http://localhost:5173",
                    "X-Title": "TaskFlow AI Assistant"
                }
            )
            
            assistant_message = response.choices[0].message
            tool_calls = assistant_message.tool_calls or []
            
            # Execute tool calls if any
            tool_results = []
            if tool_calls and tool_handler:
                for tool_call in tool_calls:
                    tool_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments or "{}")
                    
                    # Execute tool
                    result = await tool_handler(tool_name, args)
                    tool_results.append({
                        "tool": tool_name,
                        "arguments": args,
                        "result": result,
                        "tool_call_id": tool_call.id,
                    })
                
                # Add assistant message with tool calls
                messages.append({
                    "role": "assistant",
                    "content": assistant_message.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            }
                        }
                        for tc in tool_calls
                    ]
                })
                
                # Add tool results
                for tool_result in tool_results:
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_result["tool_call_id"],
                        "content": json.dumps(tool_result["result"]),
                    })
                
                # Get final response after tool execution
                follow_up = self.client.chat.completions.create(
                    model=self.config.model,
                    messages=messages,
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens,
                    extra_headers={
                        "HTTP-Referer": "http://localhost:5173",
                        "X-Title": "TaskFlow AI Assistant"
                    }
                )
                final_content = follow_up.choices[0].message.content or ""
            else:
                final_content = assistant_message.content or ""
            
            return AgentResponse(
                content=final_content,
                tool_calls=tool_results,
                model=self.config.model,
            )
            
        except Exception as e:
            return AgentResponse(
                content=f"I encountered an error: {str(e)}",
                tool_calls=[],
                model=self.config.model,
                error=str(e),
            )


@dataclass
class AgentResponse:
    """Response from the AI agent."""
    content: str
    tool_calls: List[Dict[str, Any]]
    model: str
    error: Optional[str] = None
