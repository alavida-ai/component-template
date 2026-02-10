import os
import time
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse

from src.observability.errors import ComponentError, ConfigurationError
from src.observability.logging import get_logger
from src.types.models import HealthResponse, RunRequest, RunResponse

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup, clean up on shutdown."""
    logger.info("starting_up")
    # TODO: Initialize database connection, warm caches, etc.
    yield
    logger.info("shutting_down")
    # TODO: Close database connections, flush metrics, etc.


app = FastAPI(title="Component", docs_url="/docs", lifespan=lifespan)


# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------


@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    correlation_id = request.headers.get("x-correlation-id", f"req-{int(time.time() * 1000)}")
    request.state.correlation_id = correlation_id
    response = await call_next(request)
    response.headers["x-correlation-id"] = correlation_id
    return response


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------


async def require_internal_auth(
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> str:
    """Validate Authorization: Internal <secret> header.

    Platform handles user-facing auth. Components only validate internal
    service-to-service auth via shared secret.
    """
    expected = os.getenv("PLATFORM_INTERNAL_SECRET")
    if not expected:
        raise ConfigurationError("PLATFORM_INTERNAL_SECRET not configured")

    if not authorization or not authorization.startswith("Internal "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = authorization.removeprefix("Internal ")
    if token != expected:
        raise HTTPException(status_code=403, detail="Invalid internal secret")

    return token


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------


@app.exception_handler(ComponentError)
async def component_error_handler(request: Request, exc: ComponentError):
    logger.error("component_error", error_type=type(exc).__name__, detail=str(exc))
    return JSONResponse(status_code=exc.status_code, content={"error": type(exc).__name__, "detail": str(exc)})


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="healthy")


@app.post("/run", status_code=202, response_model=RunResponse, dependencies=[Depends(require_internal_auth)])
async def run(request: RunRequest, req: Request):
    correlation_id = getattr(req.state, "correlation_id", "unknown")
    logger.info("run_received", correlation_id=correlation_id, input_keys=list(request.input.keys()) if request.input else [])

    # TODO: Replace with actual pipeline invocation (Inngest event send)
    return RunResponse(
        run_id=correlation_id,
        status="accepted",
        message="Run accepted for processing",
    )


# Mount Inngest serve endpoint only when signing key is configured
if os.getenv("INNGEST_SIGNING_KEY"):
    import inngest.fast_api
    from src.workflows.inngest_client import inngest_client

    inngest.fast_api.serve(app, inngest_client, [])
