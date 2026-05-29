# AI Business Operations Manager - Phase 2 Backend

## Overview
Phase 2 of the AI Business Operations Manager implements a production-ready, asynchronous FastAPI backend. It features persistent storage using PostgreSQL (Supabase), secure JWT authentication, and a clean, layered service-repository architecture designed for scalability and maintainability.

## Architecture
- **FastAPI**: Asynchronous REST API framework.
- **PostgreSQL**: Primary database.
- **SQLAlchemy Async**: ORM for database abstraction.
- **Pydantic v2**: Data validation.
- **JWT**: Secure token-based authentication.

## Project Structure
```
phase-02/
├── app/
│   ├── api/                    # REST API routes (Auth, Chat, CRM, Logs)
│   ├── core/                   # Security, JWT, and shared dependencies
│   ├── db/                     # Database models and session management
│   ├── repositories/           # Data access layer (CRUD operations)
│   ├── services/               # Business logic layer
│   ├── schemas/                # Pydantic validation models
│   ├── orchestration/          # Multi-agent workflow logic
│   ├── agents/                 # AI Agent definitions
│   └── tools/                  # Agent tools (CRM, Knowledge Base)
├── tests/                      # Unit and integration tests
├── alembic/                    # Database migrations
├── .env                        # Environment variables
├── requirements.txt            # Project dependencies
└── alembic.ini                 # Alembic configuration
```

## Setup & Installation

1. **Environment**: Ensure Python 3.12+ is installed.
2. **Dependencies**: 
   ```bash
   pip install -r requirements.txt
   ```
3. **Database**: Configure your `.env` with the appropriate `DATABASE_URL` (using `postgresql+asyncpg` for async support).
4. **Database Initialization**:
   ```bash
   python init_db.py
   ```
5. **Run the Server**:
   ```bash
   uvicorn app.main:app --reload
   ```

## Key API Endpoints
- **POST /api/v1/auth/register**: User registration
- **POST /api/v1/auth/login**: JWT Authentication
- **POST /api/v1/chat/message**: Main AI interaction endpoint
- **GET /api/v1/customers**: CRM Lead management
- **GET /api/v1/tickets**: Support ticket management
- **GET /api/v1/logs**: Real-time execution logs for agents

## Features
- **Multi-Agent Orchestration**: Integrated backend logic for Sales, PM, and Support agents.
- **Real-time Logging**: Captures agent "thoughts" and actions for transparency.
- **Secure Auth**: JWT-based authentication for all protected routes.
- **Persistent Memory**: Session history and CRM data stored in PostgreSQL.
