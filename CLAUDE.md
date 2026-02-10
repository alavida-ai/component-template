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

**Before marking any ticket or task as complete, you MUST run these checks.** Tests passing is NOT sufficient — the test suite mocks external boundaries. These checks verify the code works against reality.

### 1. Import Check (~2 seconds)
Catches missing imports, circular imports, NameError at import time.
```bash
uv run python -c "import src.api.server"
```

### 2. Server Boot Check (~5 seconds)
Catches config errors, env var issues, startup crashes.
```bash
make smoke
```
This imports all modules, boots the server, and curls `/health`.

### 3. Unit + Contract Tests
```bash
make test
```
Runs `pytest tests/` — includes component contract tests.

### 4. Environment Variable Check
Any new `os.environ` or `os.getenv` calls MUST be added to `.env.example`. Verify:
```bash
grep -rohP 'os\.environ\[\"(\w+)\"\]|os\.getenv\(\"(\w+)\"' src/ | sort -u
```

### 5. Inngest Workflow Check (if workflows modified)
Use the Inngest MCP server to verify workflows execute correctly:
- `list_functions` — confirm your function is registered
- `send_event` — trigger a test event
- `get_run_status` / `poll_run_status` — verify all steps complete

### 6. Database Check (if schema/models modified)
```bash
uv run alembic current
```

### 7. Manual Verification
**Tests passing is NOT sufficient.** After tests pass:
- Start the server: `make dev`
- Hit `/health` — should return `{"status": "healthy"}`
- Hit `/run` with a test payload — verify the response makes sense
- Check `tmp/logs/` for structured log output

## Debugging Protocol

**When e2e tests fail, follow this order. Do not skip steps.**

### 1. Inngest MCP first
Use Inngest MCP tools (`get_run_status`, `poll_run_status`) for workflow step errors. This gives structured step-level errors — which step failed, the exact error message.

### 2. Read the server log
Inngest executes workflow steps by calling the FastAPI server. Python tracebacks appear in the server log, not Inngest's log.

### 3. Search broadly, never narrowly
When searching logs, ALWAYS use broad patterns:
```
Traceback|Error|Exception|TypeError|ValueError|NameError|ImportError|KeyError|AttributeError|failed
```
NEVER use domain-specific patterns. These filter out the actual tracebacks.

### 4. Pre-e2e smoke tests
Before sending any real job, verify the basics:
```bash
uv run python -c "import src.api.server"
uv run python -c "from src.database.connection import engine; print('DB OK' if engine else 'No DB configured')"
```

## Component Contract

Every platform component must expose:

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/health` | GET | None | Returns `{"status": "healthy"}` + dependency checks |
| `/run` | POST | `Authorization: Internal <secret>` | Accepts `RunRequest`, returns 202 + tracks async execution |

See `src/types/models.py` for request/response schemas.

## Development

```bash
# First time setup
uv sync --all-extras
npm install
cp .env.example .env  # Then fill in values

# Daily development
make dev              # Start server with hot reload
make test             # Run tests
make smoke            # Full smoke test
make format           # Format code (black)
make lint             # Lint code (ruff)
make typecheck        # Type check (mypy)
```

## Key Patterns

- **Imports**: Use `src.` prefix from repo root (e.g., `from src.api.server import app`)
- **Internal auth**: `Authorization: Internal <secret>` — platform handles user-facing auth
- **Errors**: Use `ComponentError` hierarchy from `src/observability/errors.py`
- **Logging**: structlog JSON — always include `correlation_id`
- **Database**: Alembic for migrations, never modify schema directly
- **Inngest**: Events follow `component/event.name` naming convention
- **Repository pattern**: Use `flush()` not `commit()` — caller manages transactions

## Agent Team Coordination

When running agent teams on this codebase:
- Define merge order explicitly in the task plan for contended files
- All repo methods use `flush()` not `commit()` — Inngest step boundary manages the transaction
- Defer docs work to post-implementation — run docs agents after code is merged and verified
- QA agents must have infrastructure ready (Inngest dev server, MCP, database) before e2e validation
