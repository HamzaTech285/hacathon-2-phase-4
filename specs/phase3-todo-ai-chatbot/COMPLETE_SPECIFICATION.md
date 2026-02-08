# Phase III: Todo AI Chatbot - Complete Specification

---

## 1. PROJECT CONSTITUTION

### 1.1 Immutable Principles

**Architecture Principles**
- **Statelessness**: The FastAPI server MUST NOT store any session state in memory. All state persists in PostgreSQL.
- **Tool-Only Interaction**: The AI agent MUST interact with the system exclusively via MCP tools. No direct database access from agent code.
- **Conversation Persistence**: Every message (user and assistant) MUST be stored in the database before response delivery.
- **Atomic Operations**: Each API request MUST be self-contained with complete conversation context loaded from DB.
- **Separation of Concerns**: MCP server, FastAPI backend, and AI agent are distinct components with clear boundaries.

**Security Constraints**
- **Authentication Required**: All chat endpoints MUST validate user identity via Better Auth.
- **User Isolation**: MCP tools MUST enforce user_id validation. Users cannot access other users' tasks.
- **Input Sanitization**: All user messages and tool inputs MUST be validated and sanitized.
- **Error Privacy**: Error messages MUST NOT leak database structure, internal paths, or sensitive system information.
- **Token Security**: JWT tokens and API keys MUST be stored in environment variables, never hardcoded.

**Quality Standards**
- **Response Time**: Chat API responses MUST return within 10 seconds for simple queries, 30 seconds for multi-step reasoning.
- **Error Handling**: All errors MUST be caught, logged, and returned with user-friendly messages.
- **Type Safety**: All Python code MUST use type hints. All database models MUST use SQLModel validation.
- **Test Coverage**: MCP tools MUST have 100% unit test coverage. API endpoints MUST have integration tests.
- **Code Clarity**: No magic strings. All configurations via environment variables or constants.

**Success Criteria**
- User can create tasks via natural language ("Add task: Buy groceries")
- User can list tasks with filters ("Show my completed tasks")
- User can update tasks ("Mark task 5 as done")
- User can delete tasks ("Delete the grocery task")
- Agent provides friendly confirmations for all actions
- Conversation history persists across sessions
- System handles errors gracefully (task not found, invalid input)
- Multi-step reasoning works (list tasks, then delete one)

---

## 2. TECHNICAL SPECIFICATION

### 2.1 System Architecture

```
┌─────────────────┐
│  OpenAI ChatKit │ (Frontend)
│   (Browser UI)  │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────────────────────────────────┐
│         FastAPI Backend (Stateless)         │
│  ┌──────────────────────────────────────┐   │
│  │  POST /api/{user_id}/chat            │   │
│  │  - Validate user_id (Better Auth)    │   │
│  │  - Load conversation from DB         │   │
│  │  - Call OpenAI Agent with tools      │   │
│  │  - Persist messages to DB            │   │
│  │  - Return response                   │   │
│  └──────────────────────────────────────┘   │
└────────┬────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│         OpenAI Agents SDK                   │
│  - Parses user intent                       │
│  - Decides which MCP tool(s) to call        │
│  - Handles multi-step reasoning             │
│  - Generates natural language responses     │
└────────┬────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│         MCP Server (Official SDK)           │
│  Exposes Tools:                             │
│  - add_task(user_id, title, description?)   │
│  - list_tasks(user_id, status)              │
│  - complete_task(user_id, task_id)          │
│  - update_task(user_id, task_id, ...)       │
│  - delete_task(user_id, task_id)            │
└────────┬────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│    Neon PostgreSQL (Serverless)             │
│  Tables:                                    │
│  - users                                    │
│  - tasks                                    │
│  - conversations                            │
│  - messages                                 │
└─────────────────────────────────────────────┘
```

### 2.2 Database Models

**User Table** (Existing)
```sql
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    role VARCHAR DEFAULT 'user'
);
```

**Task Table** (Existing)
```sql
CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES user(id),
    title VARCHAR NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    due_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**Conversation Table** (New)
```sql
CREATE TABLE conversation (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES user(id),
    title VARCHAR,  -- Auto-generated from first message
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_conversation_user ON conversation(user_id);
```

**Message Table** (New)
```sql
CREATE TABLE message (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversation(id) ON DELETE CASCADE,
    role VARCHAR NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    tool_calls JSONB,  -- Stores tool call details
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_message_conversation ON message(conversation_id);
CREATE INDEX idx_message_created ON message(created_at);
```

**SQLModel Definitions**

```python
# backend/src/models/conversation.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    title: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", nullable=False)
    role: str = Field(sa_column_kwargs={"nullable": False})  # user, assistant, system
    content: str = Field(sa_column_kwargs={"nullable": False})
    tool_calls: Optional[dict] = Field(default=None, sa_column_kwargs={"type_": "JSONB"})
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### 2.3 MCP Tool Definitions

**Tool 1: add_task**
```python
@mcp.tool()
async def add_task(
    user_id: int,
    title: str,
    description: Optional[str] = None
) -> dict:
    """
    Add a new task for the user.
    
    Args:
        user_id: The ID of the user
        title: Task title (required)
        description: Optional task description
    
    Returns:
        {"success": True, "task_id": int, "title": str}
        or
        {"success": False, "error": str}
    """
```

**Tool 2: list_tasks**
```python
@mcp.tool()
async def list_tasks(
    user_id: int,
    status: str = "all"  # all, pending, completed
) -> dict:
    """
    List tasks for the user with optional status filter.
    
    Args:
        user_id: The ID of the user
        status: Filter by status (all, pending, completed)
    
    Returns:
        {
            "success": True,
            "tasks": [
                {"id": int, "title": str, "is_completed": bool, "description": str},
                ...
            ],
            "count": int
        }
        or
        {"success": False, "error": str}
    """
```

**Tool 3: complete_task**
```python
@mcp.tool()
async def complete_task(
    user_id: int,
    task_id: int
) -> dict:
    """
    Mark a task as completed.
    
    Args:
        user_id: The ID of the user
        task_id: The ID of the task to complete
    
    Returns:
        {"success": True, "task_id": int, "title": str}
        or
        {"success": False, "error": "Task not found"}
    """
```

**Tool 4: update_task**
```python
@mcp.tool()
async def update_task(
    user_id: int,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> dict:
    """
    Update task title and/or description.
    
    Args:
        user_id: The ID of the user
        task_id: The ID of the task to update
        title: New title (optional)
        description: New description (optional)
    
    Returns:
        {"success": True, "task_id": int, "updated_fields": [str]}
        or
        {"success": False, "error": "Task not found"}
    """
```

**Tool 5: delete_task**
```python
@mcp.tool()
async def delete_task(
    user_id: int,
    task_id: int
) -> dict:
    """
    Delete a task.
    
    Args:
        user_id: The ID of the user
        task_id: The ID of the task to delete
    
    Returns:
        {"success": True, "task_id": int, "title": str}
        or
        {"success": False, "error": "Task not found"}
    """
```

### 2.4 API Behavior

**Endpoint: POST /api/chat**

Request:
```json
{
    "user_id": 123,
    "conversation_id": 456,  // Optional, creates new if omitted
    "message": "Add a task to buy groceries tomorrow"
}
```

Response:
```json
{
    "conversation_id": 456,
    "response": "I've added a task for you: 'Buy groceries tomorrow'. Task ID is 789.",
    "tool_calls": [
        {
            "tool": "add_task",
            "arguments": {
                "user_id": 123,
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

**Request Flow**
1. Validate `user_id` against Better Auth session
2. If `conversation_id` is null, create new Conversation record
3. Store user message in Message table
4. Load last 10 messages from conversation as context
5. Send to OpenAI Agent with MCP tools available
6. Agent processes intent and calls appropriate tools
7. Store assistant message with tool_calls in Message table
8. Return response

**Error Handling**
- 401 Unauthorized: Invalid user_id or session
- 400 Bad Request: Missing required fields
- 404 Not Found: Conversation not found
- 500 Internal Server Error: Database or agent errors

### 2.5 Agent Behavior Rules

**Intent Detection**
- "Add", "Create", "New task" → add_task
- "List", "Show", "What are my tasks" → list_tasks
- "Complete", "Done", "Finish", "Mark as done" → complete_task
- "Update", "Change", "Rename", "Edit" → update_task
- "Delete", "Remove" → delete_task

**Natural Language Patterns**
```
User: "Add task: Buy milk"
Agent: add_task(user_id, "Buy milk", None)
Response: "✅ Added task: 'Buy milk'"

User: "Show my tasks"
Agent: list_tasks(user_id, "all")
Response: "You have 3 tasks:\n1. Buy milk (pending)\n2. Call mom (pending)\n3. Finish report (completed)"

User: "Mark task 1 as done"
Agent: complete_task(user_id, 1)
Response: "✅ Marked 'Buy milk' as completed!"

User: "Delete the milk task"
Agent: list_tasks(user_id, "all") → find task with "milk" → delete_task(user_id, 1)
Response: "✅ Deleted task: 'Buy milk'"
```

**Error Handling Patterns**
```
User: "Complete task 999"
Agent: complete_task(user_id, 999) → {"success": False, "error": "Task not found"}
Response: "❌ I couldn't find task #999. Use 'show tasks' to see your task list."

User: "Akdjfh ksjdfh"
Agent: No tool call
Response: "I'm not sure what you'd like me to do. I can help you:\n- Add tasks\n- List tasks\n- Complete tasks\n- Update tasks\n- Delete tasks\n\nWhat would you like to do?"
```

### 2.6 Acceptance Criteria

**Scenario 1: Add Task**
```
User: "Add task: Buy groceries"
Expected Tool Call: add_task(user_id=1, title="Buy groceries", description=None)
Expected Response: Contains "Buy groceries" and confirmation
```

**Scenario 2: List Tasks with Filter**
```
User: "Show my completed tasks"
Expected Tool Call: list_tasks(user_id=1, status="completed")
Expected Response: Lists only completed tasks or "No completed tasks found"
```

**Scenario 3: Complete Task**
```
User: "Mark task 5 as done"
Expected Tool Call: complete_task(user_id=1, task_id=5)
Expected Response: Confirmation with task title
```

**Scenario 4: Update Task**
```
User: "Rename task 3 to 'Call dentist'"
Expected Tool Call: update_task(user_id=1, task_id=3, title="Call dentist")
Expected Response: Confirmation with old and new title
```

**Scenario 5: Delete Task**
```
User: "Delete task 2"
Expected Tool Call: delete_task(user_id=1, task_id=2)
Expected Response: Confirmation with deleted task title
```

**Scenario 6: Multi-Step Reasoning**
```
User: "Show my tasks and delete the first one"
Expected Tool Calls: 
  1. list_tasks(user_id=1, status="all")
  2. delete_task(user_id=1, task_id=<first_task_id>)
Expected Response: Shows tasks, then confirms deletion
```

**Scenario 7: Error Handling**
```
User: "Complete task 999"
Expected Tool Call: complete_task(user_id=1, task_id=999)
Tool Response: {"success": False, "error": "Task not found"}
Expected Response: User-friendly error message
```

**Scenario 8: Conversation Persistence**
```
Request 1: User sends message → conversation_id created
Request 2: User sends another message with same conversation_id → history loaded
Expected: Agent can reference previous messages in context
```

---

## 3. IMPLEMENTATION PLAN

### 3.1 Phase Overview

**Phase 3A: Database Extensions** (1 day)
- Add Conversation and Message models
- Create migrations
- Test CRUD operations

**Phase 3B: MCP Server** (2 days)
- Set up MCP SDK
- Implement 5 task tools
- Unit test all tools
- Document tool schemas

**Phase 3C: FastAPI Chat Endpoint** (2 days)
- Implement POST /api/chat
- Integrate OpenAI Agents SDK
- Connect MCP tools to agent
- Handle conversation persistence

**Phase 3D: Agent Configuration** (1 day)
- Configure agent system prompt
- Define tool-calling behavior
- Implement error handling
- Test multi-step reasoning

**Phase 3E: ChatKit Integration** (1 day)
- Configure ChatKit with domain allowlist
- Set up API endpoint
- Test end-to-end flow
- Deploy to production

### 3.2 Detailed Steps

#### Phase 3A: Database Extensions

**Step 1: Create Models**
```bash
# File: backend/src/models/conversation.py
# File: backend/src/models/message.py
```

**Step 2: Create Migration**
```bash
cd backend
python create_migration.py --name "add_conversation_tables"
```

**Step 3: Apply Migration**
```bash
python init_db_fixed.py
```

**Step 4: Test Models**
```python
# File: backend/tests/unit/test_conversation_models.py
# - Test Conversation CRUD
# - Test Message CRUD
# - Test foreign key constraints
```

#### Phase 3B: MCP Server

**Step 1: Install MCP SDK**
```bash
pip install mcp anthropic-sdk
```

**Step 2: Create MCP Server Structure**
```
backend/src/mcp/
├── __init__.py
├── server.py          # MCP server initialization
├── tools/
│   ├── __init__.py
│   ├── task_tools.py  # All 5 task tools
│   └── schemas.py     # Tool input/output schemas
└── utils.py           # Database helpers
```

**Step 3: Implement Tools**
```python
# File: backend/src/mcp/tools/task_tools.py
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

mcp_server = Server("todo-task-tools")

@mcp_server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(name="add_task", ...),
        Tool(name="list_tasks", ...),
        Tool(name="complete_task", ...),
        Tool(name="update_task", ...),
        Tool(name="delete_task", ...),
    ]

@mcp_server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "add_task":
        return await add_task(**arguments)
    # ... other tools
```

**Step 4: Test MCP Server**
```python
# File: backend/tests/unit/test_mcp_tools.py
# - Test add_task with valid input
# - Test add_task with missing title
# - Test list_tasks with all statuses
# - Test complete_task with valid/invalid task_id
# - Test update_task partial updates
# - Test delete_task with user isolation
```

#### Phase 3C: FastAPI Chat Endpoint

**Step 1: Install OpenAI Agents SDK**
```bash
pip install openai agents-sdk
```

**Step 2: Create Chat Router**
```python
# File: backend/src/api/chat_router.py
from fastapi import APIRouter, Depends
from ..services.chat_service import ChatService
from ..auth_handler import get_current_user

chat_router = APIRouter(prefix="/chat", tags=["chat"])

@chat_router.post("")
async def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    return await ChatService.process_message(request, current_user)
```

**Step 3: Create Chat Service**
```python
# File: backend/src/services/chat_service.py
class ChatService:
    @staticmethod
    async def process_message(request: ChatRequest, user: dict):
        # 1. Get or create conversation
        # 2. Save user message
        # 3. Load conversation history
        # 4. Call OpenAI Agent with MCP tools
        # 5. Save assistant message
        # 6. Return response
```

**Step 4: Integrate Agent**
```python
# File: backend/src/services/agent_service.py
from openai import OpenAI
from mcp import ClientSession

class AgentService:
    @staticmethod
    async def run_agent(messages: list, user_id: int):
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Connect to MCP server
        async with mcp_session() as session:
            tools = await session.list_tools()
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            
            # Handle tool calls
            if response.choices[0].message.tool_calls:
                tool_results = []
                for tool_call in response.choices[0].message.tool_calls:
                    result = await session.call_tool(
                        tool_call.function.name,
                        json.loads(tool_call.function.arguments)
                    )
                    tool_results.append(result)
                
                # Send tool results back to agent for final response
                messages.append(response.choices[0].message)
                messages.append({
                    "role": "tool",
                    "content": tool_results
                })
                
                final_response = client.chat.completions.create(
                    model="gpt-4",
                    messages=messages
                )
                return final_response
            
            return response
```

**Step 5: Test Chat Endpoint**
```python
# File: backend/tests/integration/test_chat_api.py
# - Test creating new conversation
# - Test continuing existing conversation
# - Test each tool via chat
# - Test multi-step reasoning
# - Test error handling
```

#### Phase 3D: Agent Configuration

**Step 1: Create System Prompt**
```python
# File: backend/src/config/agent_config.py
SYSTEM_PROMPT = """
You are a helpful task management assistant. You help users manage their todo tasks.

You can:
- Add new tasks
- List tasks (all, pending, or completed)
- Mark tasks as completed
- Update task details
- Delete tasks

When users ask you to perform actions, use the available tools. Always confirm actions in a friendly, natural way.

If a task ID is not provided but needed, ask the user or try to infer from context.

Be concise but friendly. Use emojis sparingly (✅ for success, ❌ for errors).
"""
```

**Step 2: Configure Tool Calling**
```python
# In agent_service.py
def prepare_messages(conversation_history: list, new_message: str):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(conversation_history[-10:])  # Last 10 messages
    messages.append({"role": "user", "content": new_message})
    return messages
```

**Step 3: Error Handling**
```python
try:
    response = await AgentService.run_agent(messages, user_id)
except OpenAIError as e:
    logger.error(f"OpenAI API error: {e}")
    return {"error": "AI service temporarily unavailable"}
except MCPError as e:
    logger.error(f"MCP tool error: {e}")
    return {"error": "Unable to process task operation"}
```

#### Phase 3E: ChatKit Integration

**Step 1: Configure CORS**
```python
# In backend/src/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://localhost:3000",
        "http://localhost:5173",
        "https://*.chatkit.app",  # ChatKit domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Step 2: Deploy Backend**
```bash
# Deploy to production (e.g., Railway, Render, Fly.io)
# Get production URL: https://your-app.railway.app
```

**Step 3: Configure ChatKit**
```
1. Go to ChatKit dashboard
2. Create new chatbot
3. Set API endpoint: https://your-app.railway.app/api/chat
4. Add domain to allowlist
5. Configure authentication (Bearer token)
6. Test in ChatKit interface
```

**Step 4: End-to-End Testing**
```
Test Cases:
1. Open ChatKit interface
2. Login as test user
3. Send: "Add task: Test ChatKit integration"
4. Verify: Task added in database
5. Send: "Show my tasks"
6. Verify: List includes new task
7. Send: "Delete that task"
8. Verify: Task removed
```

### 3.3 Dependencies

**Python Packages**
```
# requirements.txt additions
mcp>=1.0.0
anthropic-sdk>=0.5.0
openai>=1.0.0
agents-sdk>=0.2.0
```

**Environment Variables**
```
# .env additions
OPENAI_API_KEY=sk-...
MCP_SERVER_URL=http://localhost:8001
CHATKIT_DOMAIN=https://your-chatbot.chatkit.app
```

### 3.4 Testing Strategy

**Unit Tests**
- MCP tools (100% coverage)
- Database models (CRUD operations)
- Chat service (message persistence)
- Agent service (tool calling logic)

**Integration Tests**
- POST /api/chat endpoint
- Conversation flow (multi-message)
- Tool execution via agent
- Error scenarios

**E2E Tests**
- ChatKit → FastAPI → Agent → MCP → Database
- User session persistence
- Multi-step task operations

**Load Tests**
- 10 concurrent users
- 100 messages/minute
- Database connection pooling
- Response time < 5s for 95th percentile

### 3.5 Deployment Checklist

- [ ] Database migrations applied to production
- [ ] Environment variables configured
- [ ] MCP server running and accessible
- [ ] FastAPI backend deployed
- [ ] OpenAI API key validated
- [ ] CORS configured for ChatKit domain
- [ ] ChatKit endpoint configured
- [ ] Health check endpoint responding
- [ ] Logs configured (structured JSON)
- [ ] Error monitoring enabled (Sentry)
- [ ] Backup strategy for database
- [ ] Rate limiting configured
- [ ] SSL/TLS enabled
- [ ] Load balancer configured (if needed)
- [ ] Documentation updated

---

## END OF SPECIFICATION

This specification is complete and ready for automated implementation via Claude Code.
