from __future__ import annotations
"""Authentication API router with signup and login endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ..database import get_session
from ..models.user import UserCreate, UserLogin
from ..services.auth import AuthService
from ..auth_handler import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from typing import Dict


auth_router = APIRouter(prefix="/auth", tags=["authentication"])


@auth_router.post("/signup", response_model=Dict[str, str])
def signup(user_data: UserCreate, db_session: Session = Depends(get_session)):
    """
    Register a new user.

    Args:
        user_data: User registration data containing email and password
        db_session: Database session for database operations

    Returns:
        Dict: Access token and token type
    """
    try:
        # Register the user
        user = AuthService.register_user(user_data, db_session)

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
            detail=f"An error occurred during registration: {str(e)}"
        )


@auth_router.post("/login", response_model=Dict[str, str])
def login(user_credentials: UserLogin, db_session: Session = Depends(get_session)):
    """
    Authenticate user and return access token.

    Args:
        user_credentials: User login credentials containing email and password
        db_session: Database session for database operations

    Returns:
        Dict: Access token and token type
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