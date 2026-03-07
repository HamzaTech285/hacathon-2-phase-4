# Feature: User Authentication

## User Stories
- As a new user, I can sign up with email and password
- As an existing user, I can log in with my credentials
- As a user, I can log out
- As a user, my password is securely hashed
- As a user, I receive a JWT token upon login

## Acceptance Criteria

### Signup
- Email must be valid format
- Password must be at least 8 characters
- Email must be unique
- Password is hashed before storage (bcrypt)
- Returns user info and JWT token

### Login
- Validates email and password
- Returns JWT token on success
- Returns 401 on invalid credentials
- Token includes user ID and expiration

### Logout
- Client removes JWT token from storage
- No server-side session management required (stateless)

### JWT Token
- Uses HS256 algorithm
- Configurable expiration (default: 30 minutes)
- Contains user ID and email
- Signed with secure secret key

## Security Requirements
- Passwords hashed with bcrypt (cost factor 12)
- JWT tokens signed with strong secret key
- Token validation on all protected endpoints
- User data isolation enforced

## Implementation Status
✅ Complete - See `backend/src/api/auth_router.py` and `backend/src/services/auth.py`
