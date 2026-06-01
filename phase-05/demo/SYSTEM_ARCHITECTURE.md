# System Architecture: Digital FTE Factory

## Overview
The system follows a modern microservices-adjacent architecture, optimized for AI-driven workflows.

```mermaid
graph TD
    User((User)) -->|HTTPS| Frontend[Next.js Frontend]
    Frontend -->|REST API| Backend[FastAPI Backend]
    
    subgraph "AI Agency Core"
        Backend --> Orchestrator[Orchestration Engine]
        Orchestrator --> Agent1[Sales Agent]
        Orchestrator --> Agent2[PM Agent]
        Orchestrator --> Agent3[Support Agent]
    end
    
    subgraph "Data Layer"
        Backend --> DB[(PostgreSQL/SQLite)]
        Backend --> Logs[Execution Logger]
    end
    
    subgraph "Intelligence"
        Agent1 --> Gemini[Google Gemini API]
        Agent2 --> Gemini
        Agent3 --> Gemini
    end
```

## Key Architectural Decisions
1.  **Frontend (Phase-03):** React-based Next.js with `standalone` Docker optimization for sub-second cold starts on Cloud Run.
2.  **Backend (Phase-04):** FastAPI with Pydantic for strict type safety and auto-generated OpenAPI documentation.
3.  **Agentic Design:** Each agent is an independent class with its own toolset (CRM tools, Knowledge tools, etc.), coordinated by a central Workflow Manager.
4.  **Security:** JWT-based authentication and protected API routes.
