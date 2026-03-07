# Phase 2 & 3 Integration Verification Checklist

## Backend Verification

### 1. Dependencies Installation
```bash
cd backend
pip install -r requirements.txt
```

**Verify:**
- [ ] `mcp>=1.0.0` installed (Official MCP SDK)
- [ ] `openai>=1.12.0` installed (OpenAI SDK for Agents)
- [ ] `fastapi>=0.109.0` installed
- [ ] `sqlmodel>=0.0.14` installed
- [ ] `python-jose[cryptography]>=3.3.0` installed
- [ ] `passlib[bcrypt]>=1.7.4` installed

### 2. Environment Configuration
```bash
cd backend
cp .env.example .env
# Edit .env with your values
```

**Verify:**
- [ ] `DATABASE_URL` set (Neon PostgreSQL connection string)
- [ ] `SECRET_KEY` set (min 32 characters)
- [ ] `OPENROUTER_API_KEY` set (from openrouter.ai)
- [ ] `ALGORITHM=HS256`
- [ ] `ACCESS_TOKEN_EXPIRE_MINUTES=30`

### 3. Database Initialization
```bash
python init_db.py
```

**Verify:**
- [ ] `user` table created
- [ ] `task` table created
- [ ] `conversation` table created
- [ ] `message` table created

### 4. Backend Server Start
```bash
uvicorn src.main:app --reload --port 8000
```

**Verify:**
- [ ] Server starts without errors
- [ ] Accessible at http://localhost:8000
- [ ] API docs at http://localhost:8000/docs
- [ ] Health check returns: http://localhost:8000/health

### 5. API Endpoint Tests

#### Authentication Endpoints
```bash
# Signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'
```

**Verify:**
- [ ] Signup returns `access_token`
- [ ] Login returns `access_token`
- [ ] Token is valid JWT format

#### Task Endpoints
```bash
# Get all tasks (requires token)
curl http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Create task
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Task", "description": "Test Description"}'
```

**Verify:**
- [ ] GET /api/tasks/ returns task list
- [ ] POST /api/tasks/ creates task
- [ ] PUT /api/tasks/{id} updates task
- [ ] DELETE /api/tasks/{id} deletes task
- [ ] All endpoints require authentication

#### Chat Endpoint
```bash
# Send chat message
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to test the system"}'
```

**Verify:**
- [ ] POST /api/chat returns response
- [ ] Response includes `conversation_id`
- [ ] Response includes `response` text
- [ ] Response includes `tool_calls` if tools were used
- [ ] AI can add tasks via natural language

### 6. MCP Server Verification

**Check MCP Server Module:**
```bash
python -c "from backend.src.mcp_server import mcp_server, TOOL_DEFINITIONS; print('MCP Server OK')"
```

**Verify:**
- [ ] MCP server imports successfully
- [ ] 5 tools defined (add_task, list_tasks, complete_task, update_task, delete_task)
- [ ] Tool schemas are valid

### 7. Agents Module Verification

**Check Agents Module:**
```bash
python -c "from backend.src.agents import TaskFlowAgent; print('Agents Module OK')"
```

**Verify:**
- [ ] TaskFlowAgent imports successfully
- [ ] AgentConfig works correctly
- [ ] OpenRouter API configuration valid

---

## Frontend Verification

### 1. Dependencies Installation
```bash
cd Frontend
npm install
```

**Verify:**
- [ ] `jwt-decode` installed
- [ ] `axios` installed
- [ ] `react` installed
- [ ] `lucide-react` installed
- [ ] shadcn/ui components installed

### 2. Environment Configuration
```bash
cd Frontend
cp .env.example .env
```

**Verify:**
- [ ] `VITE_API_URL=http://localhost:8000` set

### 3. Frontend Server Start
```bash
npm run dev
```

**Verify:**
- [ ] Server starts without errors
- [ ] Accessible at http://localhost:5173
- [ ] No console errors in browser

### 4. Frontend Functionality Tests

#### Authentication Flow
1. Navigate to http://localhost:5173
2. Click "Sign Up"
3. Create account with email/password
4. Verify redirect to dashboard

**Verify:**
- [ ] Signup form works
- [ ] Login form works
- [ ] JWT token stored in localStorage
- [ ] Token is valid JWT format
- [ ] Auth state persists on refresh

#### Task Management
1. Click "New Task"
2. Create a task with title and description
3. Verify task appears in list
4. Click checkbox to mark complete
5. Click edit button to modify task
6. Click delete button to remove task

**Verify:**
- [ ] Create task works
- [ ] List tasks works
- [ ] Update task works
- [ ] Delete task works
- [ ] Mark complete works
- [ ] UI updates immediately (optimistic updates)

#### AI Chat
1. Click chat button (bottom-right)
2. Type "Add a task to buy groceries"
3. Verify task created
4. Type "Show my tasks"
5. Verify task list shown

**Verify:**
- [ ] Chat panel opens
- [ ] Messages send successfully
- [ ] AI responses display
- [ ] Tool calls execute correctly
- [ ] Conversation persists
- [ ] Error handling works

---

## Integration Tests

### Test 1: End-to-End Task Creation via Chat
```bash
# 1. Login and get token
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}' \
  | jq -r '.access_token')

# 2. Send chat message to create task
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to test integration"}'

# 3. Verify task was created
curl http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer $TOKEN"
```

**Expected:**
- [ ] Chat response confirms task creation
- [ ] Task appears in task list
- [ ] Task has correct title

### Test 2: Multi-Turn Conversation
```bash
# 1. First message - create task
RESPONSE1=$(curl -s -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy milk"}')

# 2. Extract conversation_id
CONVERSATION_ID=$(echo $RESPONSE1 | jq -r '.conversation_id')

# 3. Second message - continue conversation
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Now show me all my tasks\", \"conversation_id\": $CONVERSATION_ID}"
```

**Expected:**
- [ ] Conversation ID preserved
- [ ] Context maintained across messages
- [ ] AI references previous interaction

### Test 3: User Data Isolation
```bash
# User 1 creates task
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer $TOKEN_USER1" \
  -H "Content-Type: application/json" \
  -d '{"title": "User 1 Task"}'

# User 2 lists tasks
curl http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer $TOKEN_USER2"
```

**Expected:**
- [ ] User 2 cannot see User 1's tasks
- [ ] User isolation enforced

---

## Performance Tests

### Response Time
- [ ] API responses < 500ms (without AI)
- [ ] Chat responses < 10s (with AI)
- [ ] Page load < 2s

### Concurrency
- [ ] Multiple users can login simultaneously
- [ ] Task operations don't block each other
- [ ] Chat conversations are isolated

---

## Security Tests

### Authentication
- [ ] Requests without token return 401
- [ ] Invalid tokens return 401
- [ ] Expired tokens return 401
- [ ] Passwords are hashed (bcrypt)

### Authorization
- [ ] Users can only see their own tasks
- [ ] Users can only update their own tasks
- [ ] Users can only delete their own tasks

### Input Validation
- [ ] Empty task titles rejected
- [ ] Long titles truncated/validated
- [ ] SQL injection attempts blocked
- [ ] XSS attempts sanitized

---

## Browser Compatibility

Test in:
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (if available)

**Verify:**
- [ ] UI renders correctly
- [ ] All features work
- [ ] No console errors

---

## Documentation Verification

**Check:**
- [ ] README.md updated
- [ ] SETUP_GUIDE.md complete
- [ ] PHASE_2_3_COMPLETION_REPORT.md accurate
- [ ] CLAUDE.md files present (root, backend, frontend)
- [ ] API documentation at /docs accessible
- [ ] Spec files in specs/ folder complete

---

## Final Checklist

### Phase 2 Requirements
- [ ] Full-stack web application working
- [ ] RESTful API endpoints functional
- [ ] Responsive frontend UI
- [ ] Database persistence (Neon PostgreSQL)
- [ ] Better Auth compatible JWT authentication
- [ ] User data isolation enforced
- [ ] Spec-Kit structure implemented

### Phase 3 Requirements
- [ ] AI chatbot interface working
- [ ] OpenAI Agents SDK integration (TaskFlowAgent)
- [ ] Official MCP SDK integration (mcp_server)
- [ ] 5 MCP tools functional
- [ ] OpenRouter API configured
- [ ] Conversation persistence working
- [ ] Natural language task management

### Code Quality
- [ ] No TypeScript errors
- [ ] No Python type errors
- [ ] All imports resolve correctly
- [ ] No console errors in browser
- [ ] Error handling in place
- [ ] Logging configured

---

## Sign-Off

**Developer:** _______________  
**Date:** _______________  
**Status:** [ ] Pass [ ] Fail  

**Notes:**
_________________________________
_________________________________
_________________________________
