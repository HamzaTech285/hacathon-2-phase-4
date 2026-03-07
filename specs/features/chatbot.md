# Feature: AI Chatbot for Task Management

## User Stories
- As a user, I can chat with an AI assistant to manage my tasks
- As a user, I can add tasks via natural language
- As a user, I can list my tasks by asking
- As a user, I can mark tasks complete via chat
- As a user, I can update or delete tasks via chat
- As a user, my conversation history is saved

## Acceptance Criteria

### Chat Interface
- POST /api/chat endpoint accepts user messages
- Returns AI response with tool call details
- Maintains conversation context across messages
- Supports creating new conversations or continuing existing ones

### Natural Language Task Management
- "Add task: Buy groceries" → Creates new task
- "Show my tasks" → Lists all tasks
- "Mark task 5 as done" → Completes task
- "Delete the grocery task" → Deletes task
- "Update task 3 to call dentist" → Updates task

### AI Agent Behavior
- Uses MCP tools for all task operations
- Provides friendly confirmations for actions
- Handles errors gracefully with helpful messages
- Can perform multi-step reasoning (list then delete)

### Conversation Persistence
- All messages stored in database
- Conversations associated with user
- Can resume conversations across sessions
- Last 10 messages used as context

## Implementation Status
✅ Complete - See `backend/src/api/chat_router.py` and `backend/src/services/chat_service.py`
