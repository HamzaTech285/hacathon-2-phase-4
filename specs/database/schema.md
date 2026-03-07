# Database Schema Specification

## Tables

### users
Stores user account information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique user ID |
| email | VARCHAR | UNIQUE, NOT NULL | User's email address |
| password_hash | VARCHAR | NOT NULL | Bcrypt hashed password |
| is_active | BOOLEAN | DEFAULT TRUE | Account status |
| role | VARCHAR | DEFAULT 'user' | User role |
| created_at | TIMESTAMP | DEFAULT NOW() | Account creation time |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update time |

**Indexes:**
- `idx_users_email` - Fast email lookup for authentication

---

### tasks
Stores todo tasks for users.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique task ID |
| user_id | INTEGER | FOREIGN KEY → users.id, NOT NULL | Task owner |
| title | VARCHAR | NOT NULL | Task title |
| description | TEXT | NULLABLE | Task description |
| is_completed | BOOLEAN | DEFAULT FALSE | Completion status |
| due_date | TIMESTAMP | NULLABLE | Task due date |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update time |

**Indexes:**
- `idx_tasks_user_id` - Fast filtering by user
- `idx_tasks_is_completed` - Fast status filtering
- `idx_tasks_user_completed` - Composite index for common queries

---

### conversations
Stores chat conversation sessions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique conversation ID |
| user_id | INTEGER | FOREIGN KEY → users.id, NOT NULL | Conversation owner |
| title | VARCHAR | NULLABLE | Auto-generated title |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update time |

**Indexes:**
- `idx_conversations_user_id` - Fast lookup by user

---

### messages
Stores chat messages within conversations.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique message ID |
| conversation_id | INTEGER | FOREIGN KEY → conversations.id, NOT NULL | Parent conversation |
| role | VARCHAR | NOT NULL, CHECK (role IN ('user', 'assistant', 'system')) | Message sender |
| content | TEXT | NOT NULL | Message content |
| tool_calls | JSONB | NULLABLE | Tool call details if any |
| created_at | TIMESTAMP | DEFAULT NOW() | Message time |

**Indexes:**
- `idx_messages_conversation_id` - Fast lookup by conversation
- `idx_messages_created_at` - Chronological ordering

---

## Relationships

```
users (1) ──────< tasks (*)
users (1) ──────< conversations (*)
conversations (1) ──────< messages (*)
```

## SQLModel Definitions

### User Model
```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(sa_column_kwargs={"nullable": False}, unique=True)
    password_hash: str = Field(sa_column_kwargs={"nullable": False})
    is_active: bool = Field(default=True)
    role: str = Field(default="user")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Task Model
```python
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", sa_column_kwargs={"nullable": False})
    title: str = Field(sa_column_kwargs={"nullable": False})
    description: Optional[str] = Field(default=None)
    is_completed: bool = Field(default=False)
    due_date: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Conversation Model
```python
class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", sa_column_kwargs={"nullable": False})
    title: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Message Model
```python
class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", sa_column_kwargs={"nullable": False})
    role: str = Field(sa_column_kwargs={"nullable": False})
    content: str = Field(sa_column_kwargs={"nullable": False})
    tool_calls: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## Implementation Status
✅ Complete - All models implemented in `backend/src/models/`
