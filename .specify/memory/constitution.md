<!-- SYNC IMPACT REPORT
Version change: N/A -> 1.0.0
Added sections: All principles and sections as per Todo app requirements
Removed sections: None
Templates requiring updates: N/A
Follow-up TODOs: None
-->

# Todo App Constitution

## Core Principles

### Frontend-First Approach
Prioritize extending and improving the existing frontend; Maintain compatibility with current frontend structure and leverage /lib/api.ts for API calls; Any new features must integrate seamlessly with existing frontend architecture.

### Backend Modern Architecture
Use FastAPI with SQLModel ORM for backend services and Neon Serverless PostgreSQL for database storage; All backend services must follow RESTful principles and maintain clean separation of concerns; Database schema changes must be properly versioned and migrated.

### Secure Authentication (NON-NEGOTIABLE)
Implement Better Auth for user authentication with JWT token validation on all REST endpoints; Every API call must validate JWT tokens issued by Better Auth before processing requests; Unauthorized access attempts must be logged and rejected with appropriate HTTP status codes.

### User Data Isolation
Ensure users can only access and modify their own tasks and data; All API endpoints must validate that requested resources belong to the authenticated user; Data access controls must be implemented at both application and database levels.

### Monorepo Organization
Organize codebase with separate frontend/ and backend/ directories maintaining clear architectural boundaries; Include CLAUDE.md file at project root with comprehensive project context and development guidelines; All new features must follow established monorepo structure conventions.

### Full-Stack Integration
Maintain tight integration between frontend and backend components while preserving loose coupling; All API contracts must be clearly defined and documented; Frontend API calls must handle backend errors gracefully and provide appropriate user feedback.

## Security & Architecture Requirements
All REST endpoints must require and validate JWTs from Better Auth; Task Management requires full CRUD functionality with proper user ownership validation; Database connections must use secure connection pooling and prepared statements; Input validation must occur at both frontend and backend layers to prevent injection attacks.

## Development Workflow
Follow Spec-Kit monorepo conventions for code organization and deployment; Implement comprehensive testing strategy covering frontend components and backend API endpoints; Conduct security reviews for all authentication and authorization changes; Maintain backward compatibility for existing API endpoints during feature development.

## Governance
This constitution governs all development activities for the Todo app; All code changes must comply with security requirements and architectural principles; Amendments require documentation of rationale and impact assessment; Code reviews must verify compliance with all stated principles before merging.

**Version**: 1.0.0 | **Ratified**: 2026-02-02 | **Last Amended**: 2026-02-02
