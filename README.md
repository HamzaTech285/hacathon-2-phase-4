# Full-Stack Todo App with Authentication

A complete full-stack Todo application with secure user authentication and task management built with FastAPI, SQLModel, React, and Neon PostgreSQL.

## 🚀 Features

- **🔐 User Authentication**: Secure registration and login with JWT tokens
- **📋 Task Management**: Create, read, update, and delete personal tasks
- **🔒 Data Isolation**: Users can only access their own tasks
- **📱 Responsive UI**: Modern web interface built with React/Next.js
- **🌐 RESTful API**: Clean API design with proper authentication
- **🛡️ Security**: Password hashing with bcrypt, JWT validation, input sanitization
- **🧪 Testing**: Comprehensive unit and integration tests

## 🛠️ Tech Stack

- **Backend**: Python 3.11, FastAPI, SQLModel, Neon PostgreSQL
- **Frontend**: TypeScript, React, Next.js
- **Authentication**: Custom JWT implementation with proper validation
- **Database**: Neon Serverless PostgreSQL with SQLModel ORM
- **Security**: Password hashing with bcrypt, JWT validation, user data isolation

## 📡 API Endpoints

### Authentication
- `POST /api/auth/signup` - Register a new user
- `POST /api/auth/login` - Login an existing user

### Tasks
- `GET /api/tasks` - Get all tasks for authenticated user
- `POST /api/tasks` - Create a new task for authenticated user
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a specific task
- `DELETE /api/tasks/{id}` - Delete a specific task

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (or access to Neon PostgreSQL)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and secret key
   ```

5. Run the application:
   ```bash
   uvicorn src.main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd Frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

## 🔐 Environment Variables

### Backend (.env)
- `DATABASE_URL` - PostgreSQL database URL
- `SECRET_KEY` - Secret key for JWT signing (use a strong random key in production)
- `ALGORITHM` - Algorithm for JWT (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time (default: 30)

## 🛡️ Security Features

- Passwords are securely hashed using bcrypt
- JWT tokens with configurable expiration times
- User data isolation - users can only access their own tasks
- Input validation at both frontend and backend
- Proper error handling without information leakage
- Rate limiting protection for authentication endpoints

## 🧪 Running Tests

Backend tests:
```bash
cd backend
source .venv/bin/activate  # Activate virtual environment
python -m pytest tests/ -v
```

## 📁 Project Structure

```
backend/
├── src/
│   ├── models/          # Database models (User, Task)
│   ├── services/        # Business logic (Auth, Task services)
│   ├── api/             # API routers (Auth, Task endpoints)
│   ├── database.py      # Database configuration
│   ├── auth_handler.py  # JWT handling utilities
│   └── main.py          # Application entry point
├── requirements.txt
└── tests/               # Unit and integration tests

Frontend/
├── src/
│   ├── components/      # React components (auth, tasks)
│   ├── pages/           # Page components (signup, login, dashboard)
│   ├── lib/             # API utilities
│   ├── utils/           # Utility functions (auth helpers)
│   └── types/           # Type definitions
├── package.json
└── README.md
```

## ✅ Implementation Status

This project is fully implemented with:
- Complete backend API with authentication and task management
- Full-featured frontend with authentication flows
- Comprehensive unit and integration tests
- Proper security measures and data isolation
- Documentation and setup guides

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📄 License

[MIT](LICENSE)