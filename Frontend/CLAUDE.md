# Frontend Guidelines

## Stack
- React 18.3+
- TypeScript 5.8+
- Vite 7.3+
- Tailwind CSS 3.4+
- shadcn/ui components
- Better Auth compatible JWT

## Project Structure
```
Frontend/
├── src/
│   ├── main.tsx             # Entry point
│   ├── App.tsx              # Root component
│   ├── index.css            # Global styles
│   ├── components/          # UI components
│   │   ├── ui/              # shadcn/ui components
│   │   ├── todo/            # Task components
│   │   ├── chat/            # Chat components
│   │   └── auth/            # Auth components
│   ├── pages/               # Page components
│   │   ├── Index.tsx
│   │   ├── dashboard.tsx
│   │   ├── auth.tsx
│   │   └── login.tsx
│   ├── lib/                 # Utilities
│   │   ├── api.ts           # API client
│   │   ├── auth-client.ts   # Better Auth client
│   │   └── utils.ts         # Helpers
│   ├── hooks/               # Custom hooks
│   │   └── useTodos.ts      # Task management hook
│   ├── services/            # API services
│   │   └── api.ts           # API service layer
│   ├── utils/               # Utilities
│   │   └── auth.ts          # Auth utilities
│   └── types/               # TypeScript types
│       └── task.ts          # Task types
├── package.json
└── .env
```

## Patterns
- Use functional components with hooks
- TypeScript for type safety
- Tailwind CSS for styling
- Client components for interactivity
- API calls through service layer

## Component Structure
- `/components` - Reusable UI components
- `/pages` - Route pages
- Use PascalCase for component names
- Export components as named exports

## API Client
All backend calls should use the API client:

```typescript
import { api } from '@/lib/api'

// Get tasks
const tasks = await api.getTasks()

// Create task
const task = await api.createTask(taskData)

// Auth header automatically included
```

## Authentication
Use Better Auth compatible JWT system:

```typescript
import { 
  login, 
  signup, 
  logout, 
  isAuthenticated,
  getAccessToken 
} from '@/lib/auth-client'

// Login
await login(email, password)

// Check auth
if (isAuthenticated()) {
  // Protected content
}

// Logout
logout()
```

## Styling
- Use Tailwind CSS classes
- No inline styles
- Follow existing component patterns
- Use shadcn/ui components as base
- Dark theme with green primary color

## Key Patterns

### Custom Hooks
```typescript
// hooks/useTodos.ts
export function useTodos() {
  const [todos, setTodos] = useState<Todo[]>([])
  const [loading, setLoading] = useState(false)

  const addTodo = async (data: TodoFormData) => {
    const task = await api.createTask(data)
    setTodos([...todos, task])
  }

  return { todos, loading, addTodo, ... }
}
```

### API Service
```typescript
// services/api.ts
class ApiService {
  async getTasks() {
    const response = await this.client.get('/tasks')
    return response.data
  }

  async createTask(data: TaskCreate) {
    const response = await this.client.post('/tasks', data)
    return response.data
  }
}

export const api = new ApiService()
```

### Auth Client
```typescript
// lib/auth-client.ts
export const login = async (email: string, password: string) => {
  const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
  
  const data = await response.json()
  setAuthTokens(data)
  return data
}
```

## Environment Variables
```bash
VITE_API_URL=http://localhost:8000
```

## Running
```bash
# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Code Style
- Use TypeScript for type safety
- Functional components with hooks
- Destructure props
- Use meaningful variable names
- Add error boundaries

## Type Definitions

### Task
```typescript
interface Todo {
  id: number
  title: string
  description?: string
  is_completed: boolean
  due_date?: string
  created_at: string
  updated_at: string
}
```

### Auth
```typescript
interface User {
  id: number
  email: string
  role: string
}

interface AuthTokens {
  access_token: string
  token_type: string
}
```

## Testing
```bash
# Run tests
npm run test

# Run tests in watch mode
npm run test:watch
```
