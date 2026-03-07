# Quick Setup Guide - Phase 2 & 3

## Prerequisites

- Python 3.11+
- Node.js 18+
- Neon PostgreSQL database (free tier at https://neon.tech)
- OpenRouter API key (free at https://openrouter.ai)

## Step 1: Backend Setup

### 1.1 Install Dependencies

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\Activate
# Linux/Mac:
source .venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 1.2 Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
```

**Required Environment Variables:**

```bash
# Database (get from Neon.tech)
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/taskflow?sslmode=require

# JWT Secret (generate a strong random string)
SECRET_KEY=your-super-secret-key-change-in-production-min-32-chars

# OpenRouter API Key (get from openrouter.ai)
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here

# Optional settings
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
```

### 1.3 Initialize Database

```bash
# Create tables
python init_db.py

# Optional: Create a test user
python create_test_user.py
```

### 1.4 Start Backend Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

API docs at: `http://localhost:8000/docs`

---

## Step 2: Frontend Setup

### 2.1 Install Dependencies

```bash
cd Frontend

# Install packages
npm install
```

### 2.2 Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env
```

**Required Environment Variables:**

```bash
# Backend API URL
VITE_API_URL=http://localhost:8000
```

### 2.3 Start Frontend Server

```bash
npm run dev
```

Frontend will be available at: `http://localhost:5173`

---

## Step 3: Test the Application

### 3.1 Create Account

1. Open `http://localhost:5173` in your browser
2. Click "Sign Up" or navigate to `/auth`
3. Enter email and password (min 8 characters)
4. Click "Create Account"

### 3.2 Login

1. Enter your email and password
2. Click "Login"
3. You'll be redirected to the dashboard

### 3.3 Create Tasks

1. Click "New Task" button
2. Fill in title (required) and description (optional)
3. Click "Create Task"

### 3.4 Use AI Chat

1. Click the chat button (bottom-right corner)
2. Try these commands:
   - "Add a task to buy groceries"
   - "Show me all my tasks"
   - "Mark task 1 as complete"
   - "What tasks do I have pending?"
   - "Delete the groceries task"

---

## Troubleshooting

### Backend Issues

**Error: "OPENROUTER_API_KEY environment variable is required"**
- Make sure `.env` file exists in `backend/` folder
- Check that `OPENROUTER_API_KEY` is set correctly
- Restart the backend after changing `.env`

**Error: "Could not connect to database"**
- Verify `DATABASE_URL` in `.env`
- Check that Neon database is active
- Ensure SSL mode is enabled: `?sslmode=require`

**Error: "Module not found"**
- Activate virtual environment: `.venv\Scripts\Activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Frontend Issues

**Error: "Cannot connect to backend"**
- Ensure backend is running on port 8000
- Check `VITE_API_URL` in `.env`
- Check browser console for CORS errors

**Error: "Module not found"**
- Run `npm install` in Frontend folder
- Clear node_modules: `rm -rf node_modules && npm install`

### Chat Issues

**AI not responding:**
- Check OpenRouter API key is valid
- Verify you have credits on OpenRouter (free tier available)
- Check backend logs for errors

**Tool calls not working:**
- Verify database has tasks table
- Check that user is authenticated
- Look at browser console for errors

---

## Get API Keys

### Neon PostgreSQL (Free)

1. Visit https://neon.tech
2. Sign up with GitHub
3. Create a new project
4. Copy connection string (Pooler mode recommended)
5. Format: `postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/dbname?sslmode=require`

### OpenRouter API (Free Tier Available)

1. Visit https://openrouter.ai
2. Sign up with Google/GitHub
3. Go to "Keys" section
4. Create a new key
5. Copy the key (starts with `sk-or-v1-`)

---

## Development Tips

### Backend Hot Reload

```bash
# Auto-restart on code changes
uvicorn src.main:app --reload
```

### Frontend Hot Reload

```bash
# Auto-refresh on code changes
npm run dev
```

### View API Documentation

Open http://localhost:8000/docs for interactive API docs (Swagger UI)

### Debug Mode

Add to `.env`:
```bash
DEBUG=True
```

### Database Inspection

```bash
# Connect to Neon database
psql "$DATABASE_URL"

# List tables
\dt

# View tasks
SELECT * FROM task;

# View conversations
SELECT * FROM conversation;
```

---

## Next Steps

### Phase 4: Kubernetes Deployment

Once Phase 2 & 3 are working, proceed to Phase 4:

```bash
# Build Docker images
docker build -t taskflow-backend ./backend
docker build -t taskflow-frontend ./Frontend

# Deploy to Minikube
./deploy.sh
```

See `PHASE4_AIOPS_COMPLETE.md` for details.

### Phase 5: Cloud Deployment (Optional)

Deploy to DigitalOcean Kubernetes with Kafka and Dapr.

---

## Support

- Check `PHASE_2_3_COMPLETION_REPORT.md` for detailed documentation
- Review `specs/` folder for feature specifications
- Check `CLAUDE.md` for development guidelines

---

**Status:** ✅ Ready for Development  
**Last Updated:** 2026-03-02
