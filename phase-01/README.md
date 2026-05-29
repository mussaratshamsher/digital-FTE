# AI Business Operations Manager - Stage 1

## Overview
This is Stage 1 of the AI Business Operations Manager, an advanced multi-agent SaaS application designed to simulate an autonomous AI workforce for businesses.

The system uses a Master Orchestrator to analyze user requests, plan workflows, and delegate tasks to specialized agents (Sales, Support, Project Management, and Content).

## Architecture
- **Master Orchestrator**: The brain of the system. Analyzes intent and plans the execution roadmap.
- **Sales Agent**: Handles lead qualification and business inquiries.
- **Support Agent**: Manages customer inquiries and support tickets.
- **Project Manager Agent**: Decomposes tasks and generates implementation roadmaps.
- **Content Agent**: Drafts professional communications and proposals.

## Tech Stack
- **Python 3.12+**
- **OpenAI Agents SDK** (via Async OpenAI client)
- **Pydantic**: Data validation and schemas.
- **Rich**: Advanced CLI logging and formatting.
- **AsyncIO**: Concurrent task execution.

## Project Structure
```
phase-01/
├── app/
│   ├── main.py                 # CLI Entry point
│   ├── agents/                 # Specialized Agent logic
│   ├── tools/                  # Agent tool definitions (CRM, KB, etc.)
│   ├── orchestration/          # Workflow and delegation engine
│   ├── memory/                 # Session and context management
│   ├── logs/                   # Execution logging (Rich)
│   ├── schemas/                # Pydantic models
│   └── config/                 # System settings
├── .env                        # Environment variables
└── requirements.txt            # Project dependencies
```

## Setup Instructions
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Ensure your `.env` file has your `OPENAI_API_KEY`.
3. Run the application:
   ```bash
   python -m app.main
   ```

## Workflow Example
1. **User Request**: "I want to start a new AI automation project for my logistics company."
2. **Orchestrator**: Analyzes request and identifies need for Sales, PM, and Content agents.
3. **Sales Agent**: Qualifies the lead and identifies logistics-specific needs.
4. **PM Agent**: Breaks down the project into a 4-week roadmap.
5. **Content Agent**: Drafts an introductory email and project proposal.
6. **Final Synthesis**: Orchestrator combines all outputs into a cohesive response.

## Future Roadmap
- **Stage 2**: Integration with real CRM and Communication APIs.
- **Stage 3**: Persistent database (PostgreSQL) and Vector Memory (Qdrant).
- **Stage 4**: FastAPI Backend and React Frontend.
