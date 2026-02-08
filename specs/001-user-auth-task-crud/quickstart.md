# Quickstart Guide: Full-Stack Todo App with Authentication

## Prerequisites

- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)
- PostgreSQL-compatible database (Neon recommended)
- Git

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup

#### Navigate to Backend Directory
```bash
cd backend
```

#### Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Set Up Environment Variables
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
SECRET_KEY=your-super-secret-key-here
NEON_DATABASE_URL=your-neon-database-url
BETTER_AUTH_SECRET=your-better-auth-secret
```

#### Run Database Migrations
```bash
alembic upgrade head
```

#### Start Backend Server
```bash
uvicorn src.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

### 3. Frontend Setup

#### Navigate to Frontend Directory
```bash
cd frontend
```

#### Install Dependencies
```bash
npm install
```

#### Set Up Environment Variables
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000/auth
```

#### Start Frontend Development Server
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /auth/signup` - Create new user account
- `POST /auth/login` - Authenticate user

### Task Management
- `GET /tasks` - Get user's tasks
- `POST /tasks` - Create new task
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task

## Development Commands

### Backend
```bash
# Run tests
pytest

# Format code
black .

# Lint code
flake8
```

### Frontend
```bash
# Run tests
npm test

# Build for production
npm run build

# Format code
npm run format

# Lint code
npm run lint
```

## Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

### End-to-End Tests
```bash
cd frontend
npm run test:e2e
```

## Environment Configuration

### Local Development
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`

### Production
- Backend: `https://api.yourdomain.com`
- Frontend: `https://yourdomain.com`

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Verify your PostgreSQL server is running
   - Check that your DATABASE_URL is correctly configured
   - Ensure your database user has proper permissions

2. **Authentication Failing**
   - Confirm that BETTER_AUTH_SECRET matches between frontend and backend
   - Check that JWT tokens are being properly sent in requests

3. **Frontend Cannot Reach Backend**
   - Verify NEXT_PUBLIC_API_BASE_URL is set correctly
   - Check CORS settings in backend configuration

### Reset Database
To reset the database to a clean state:
```bash
cd backend
alembic downgrade base
alembic upgrade head
```