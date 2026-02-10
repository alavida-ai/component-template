# {{COMPONENT_NAME}}

> **Replace this file** with your component's identity after creating from template.

## Identity

| Attribute | Value |
|-----------|-------|
| **Component** | {{COMPONENT_NAME}} |
| **Type** | Platform Component |
| **Owner** | {{OWNER}} |
| **Stack** | Python 3.12, FastAPI, SQLAlchemy, Inngest |

## Purpose

{{One sentence describing what this component does.}}

## Tech Stack

- **API:** FastAPI (async)
- **Database:** PostgreSQL via async SQLAlchemy + asyncpg
- **Workflows:** Inngest (event-driven)
- **Logging:** structlog (JSON)
- **Migrations:** Alembic

## Verification Protocol

Run these in order. All must pass before a task is considered done.

### 1. Smoke Test
```bash
make smoke
```
This imports all modules, boots the server, and curls `/health`.

### 2. Unit + Contract Tests
```bash
make test
```
Runs `pytest tests/` — includes component contract tests.

### 3. Manual Verification

**Tests passing is NOT sufficient.** After tests pass:
- Start the server: `make dev`
- Hit `/health` — should return `{"status": "healthy"}`
- Hit `/run` with a test payload — verify the response makes sense
- Check `tmp/logs/` for structured log output

## Component Contract

Every platform component must expose:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Returns `{"status": "healthy"}` + dependency checks |
| `/run` | POST | Accepts `RunRequest`, returns 202 + tracks async execution |

See `src/types/models.py` for request/response schemas.

## Development

```bash
# First time setup
uv sync
npm install
cp .env.example .env  # Then fill in values

# Daily development
make dev              # Start server with hot reload
make test             # Run tests
make smoke            # Full smoke test
```

## Conventions

- All errors use `ComponentError` hierarchy from `src/observability/errors.py`
- Structured logging via `structlog` — always include `correlation_id`
- Database migrations via Alembic — never modify schema directly
- Inngest events follow `component/event.name` naming convention
