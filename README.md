# Component Template

Python boilerplate for Alavida platform components.

## Quick Start

1. **Create from template:**
   - Click "Use this template" on GitHub, or
   - `gh repo create your-org/your-component --template alavida-ai/component-template`

2. **Setup:**
   ```bash
   uv sync
   npm install
   cp .env.example .env
   ```

3. **Configure:**
   - Edit `CLAUDE.md` — replace placeholders with your component identity
   - Edit `pyproject.toml` — update name, description
   - Edit `.env` — add your database URL and secrets

4. **Develop:**
   ```bash
   make dev    # Start server with hot reload
   make test   # Run tests
   make smoke  # Full smoke test
   ```

## What's Included

- **FastAPI server** with `/health` and `/run` endpoints
- **Async SQLAlchemy** database setup with Alembic migrations
- **Inngest** workflow client for event-driven pipelines
- **structlog** JSON logging with correlation IDs
- **Component error hierarchy** for consistent error handling
- **Contract tests** verifying component interface compliance
- **Makefile** with `smoke`, `test`, `dev` targets
- **Compound engineering plugin** pre-configured via `.claude/settings.json`

## Structure

```
src/
├── api/server.py              # FastAPI app: /run, /health
├── pipelines/interface.py     # Abstract pipeline interface
├── workflows/inngest_client.py # Inngest client + events
├── database/connection.py     # Async SQLAlchemy setup
├── observability/
│   ├── logging.py             # structlog configuration
│   ├── errors.py              # ComponentError hierarchy
│   └── usage_metrics.py       # Token/cost tracking
└── types/models.py            # Pydantic models
```

## Deployment

Pre-configured for Railway deployment via `railway.json`.
