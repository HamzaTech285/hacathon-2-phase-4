# Backend Guidelines

## Stack
- FastAPI 0.109+
- SQLModel 0.0.14 (ORM)
- Neon Serverless PostgreSQL
- Official MCP SDK
- OpenAI Agents SDK
- OpenRouter API

## Project Structure
```
backend/
├── src/
│   ├── main.py              # FastAPI app entry point
│   ├── auth_handler.py      # JWT authentication
│   ├── database.py          # Database connection
│   ├── models/              # SQLModel database models
│   │   ├── user.py
│   │   ├── task.py
│   │   └── conversation.py
│   ├── services/            # Business logic
│   │   ├── auth.py
│   │   ├── task_service.py
│   │   └── chat_service.py
│   ├── api/                 # API route handlers
│   │   ├── auth_router.py
│   │   ├── task_router.py
│   │   └── chat_router.py
│   ├── mcp_server/          # Official MCP Server
│   │   ├── server.py
│   │   └── tools.py
│   └── agents/              # OpenAI Agents SDK
│       ├── __init__.py
│       └── taskflow_agent.py
├── requirements.txt
└── .env
```

## API Conventions
- All routes under `/api/`
- Return JSON responses
- Use Pydantic models for request/response
- Handle errors with HTTPException
- Validate JWT on all protected endpoints

## Database
- Use SQLModel for all database operations
- Connection string from environment variable: `DATABASE_URL`
- All queries filtered by `user_id` for user isolation
- Use sessions for transaction management

## Authentication
- JWT tokens with HS256 algorithm
- Secret key from `SECRET_KEY` environment variable
- Token expiration: 30 minutes (configurable)
- Better Auth compatible JWT format
- Use `get_current_user` dependency for protected routes

## MCP Server
- Built with official MCP SDK
- Tools defined in `mcp_server/server.py`
- Tool execution in `mcp_server/tools.py`
- 5 tools: add_task, list_tasks, complete_task, update_task, delete_task
- All tools enforce user isolation

## AI Agents
- TaskFlowAgent in `agents/taskflow_agent.py`
- Uses OpenAI Agents SDK patterns
- Configured for OpenRouter API
- Model: `openai/gpt-4o-mini`
- Temperature: 0.2
- Max tokens: 500

## Running
```bash
# Activate virtual environment
.venv\Scripts\Activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac

# Run server
uvicorn src.main:app --reload --port 8000

# Run with auto-reload
uvicorn src.main:app --reload
```

## Environment Variables
```bash
DATABASE_URL=postgresql://user:pass@host/dbname?sslmode=require
SECRET_KEY=your-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENROUTER_API_KEY=sk-or-v1-your-key
DEBUG=True
```

## Testing
```bash
# Run tests
pytest tests/ -v

# Run specific test file
pytest tests/integration/test_task_api.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Code Style
- Use type hints for all functions
- Follow PEP 8 guidelines
- Use docstrings for public methods
- Keep functions small and focused
- Handle errors gracefully

## Key Patterns

### Dependency Injection
```python
from fastapi import Depends
from sqlmodel import Session

@router.get("/tasks")
def get_tasks(
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    # User ID from JWT token
    user_id = current_user["user_id"]
    # ...
```

### Service Layer
```python
class TaskService:
    @staticmethod
    def create_task(task_data: TaskCreate, session: Session) -> Task:
        task = Task.from_orm(task_data)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
```

### Error Handling
```python
from fastapi import HTTPException, status

try:
    task = TaskService.get_task(task_id, user_id, session)
except TaskNotFoundError:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )
```
