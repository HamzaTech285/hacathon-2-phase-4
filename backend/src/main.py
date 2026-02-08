from __future__ import annotations
"""
Main entry point for the Todo Application backend.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from .api.auth_router import auth_router
from .api.task_router import task_router
from .api.chat_router import chat_router
from .database import get_session
from .models.user import UserLogin
from .services.auth import AuthService
from .auth_handler import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from typing import Dict

app = FastAPI(title="Todo App API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(task_router, prefix="/api")
app.include_router(chat_router, prefix="/api")

# Add a direct login route at root level for convenience
@app.post("/login", response_model=Dict[str, str])
def root_login(user_credentials: UserLogin, db_session: Session = Depends(get_session)):
    """
    Authenticate user and return access token at root level.
    This duplicates the functionality of /api/auth/login for convenience.
    """
    try:
        # Authenticate the user
        user = AuthService.authenticate_user(
            user_credentials.email,
            user_credentials.password,
            db_session
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user account",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = AuthService.create_access_token_for_user(
            user, expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during login: {str(e)}"
        )

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo App API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Todo App API is running"}