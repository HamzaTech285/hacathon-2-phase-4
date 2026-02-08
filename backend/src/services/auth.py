"""Authentication service for user registration, login, and JWT handling."""

from sqlmodel import Session, select
from typing import Optional
from datetime import timedelta
from ..models.user import User, UserCreate, UserLogin
from ..auth_handler import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException, status


class AuthService:
    """Service class for authentication operations."""

    @staticmethod
    def register_user(user_data: UserCreate, db_session: Session) -> User:
        """
        Register a new user.

        Args:
            user_data: User creation data containing email and password
            db_session: Database session for database operations

        Returns:
            User: The created user object

        Raises:
            HTTPException: If email already exists
        """
        # Check if user with email already exists
        existing_user = db_session.exec(
            select(User).where(User.email == user_data.email)
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash the password
        password_hash = get_password_hash(user_data.password)

        # Create new user
        db_user = User(
            email=user_data.email,
            password_hash=password_hash
        )

        # Add to database
        db_session.add(db_user)
        db_session.commit()
        db_session.refresh(db_user)

        return db_user

    @staticmethod
    def authenticate_user(email: str, password: str, db_session: Session) -> Optional[User]:
        """
        Authenticate a user by email and password.

        Args:
            email: User's email address
            password: User's plain text password
            db_session: Database session for database operations

        Returns:
            User: The authenticated user object if credentials are valid, None otherwise
        """
        # Find user by email
        user = db_session.exec(
            select(User).where(User.email == email)
        ).first()

        # Verify user exists and password is correct
        if not user or not verify_password(password, user.password_hash):
            return None

        return user

    @staticmethod
    def create_access_token_for_user(user: User, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create an access token for a user.

        Args:
            user: The user for whom to create the token
            expires_delta: Optional expiration time for the token

        Returns:
            str: The JWT access token
        """
        data = {"sub": user.email, "user_id": user.id}
        return create_access_token(data=data, expires_delta=expires_delta)

    @staticmethod
    def get_user_by_email(email: str, db_session: Session) -> Optional[User]:
        """
        Retrieve a user by their email address.

        Args:
            email: User's email address
            db_session: Database session for database operations

        Returns:
            User: The user object if found, None otherwise
        """
        user = db_session.exec(
            select(User).where(User.email == email)
        ).first()

        return user