"""Shared test fixtures for platform components.

Provides:
- Async SQLite test database (no PostgreSQL needed for unit/integration tests)
- FastAPI TestClient with Inngest mocked
- Internal auth fixtures
- Sample data factories
"""

from __future__ import annotations

import os
from typing import Any, AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Set test environment variables BEFORE any src imports
os.environ.setdefault("PLATFORM_INTERNAL_SECRET", "test-secret-123")
os.environ.setdefault("INNGEST_DEV", "1")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

from src.api.server import app


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
TEST_INTERNAL_SECRET = "test-secret-123"


# ---------------------------------------------------------------------------
# HTTP client fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
async def client():
    """Unauthenticated HTTP client for health checks etc."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def authed_client():
    """HTTP client with valid internal auth header."""
    headers = {"Authorization": f"Internal {TEST_INTERNAL_SECRET}"}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test", headers=headers) as ac:
        yield ac


# ---------------------------------------------------------------------------
# Database fixtures
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture
async def test_db_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Async SQLite in-memory engine for unit tests.

    SQLite doesn't support schemas, so only creates tables with no schema set.
    Schema-based tables need PostgreSQL (integration/e2e tests).
    """
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    # TODO: Uncomment when you have SQLAlchemy models:
    # from src.database.models import Base
    # async with engine.begin() as conn:
    #     await conn.run_sync(
    #         lambda sync_conn: Base.metadata.create_all(
    #             sync_conn,
    #             tables=[t for t in Base.metadata.sorted_tables if t.schema is None],
    #         )
    #     )

    yield engine

    # TODO: Uncomment when you have SQLAlchemy models:
    # async with engine.begin() as conn:
    #     await conn.run_sync(
    #         lambda sync_conn: Base.metadata.drop_all(
    #             sync_conn,
    #             tables=[t for t in Base.metadata.sorted_tables if t.schema is None],
    #         )
    #     )

    await engine.dispose()


@pytest_asyncio.fixture
async def test_db_session(test_db_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Async session that auto-rolls-back after each test."""
    session_factory = sessionmaker(
        test_db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with session_factory() as session:
        yield session
        await session.rollback()


# ---------------------------------------------------------------------------
# Inngest mock fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_inngest_client() -> MagicMock:
    """Mock Inngest client that captures sent events."""
    client = MagicMock()
    client.send = AsyncMock(return_value=None)
    return client


# ---------------------------------------------------------------------------
# Auth fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def valid_internal_auth_header() -> dict[str, str]:
    """Valid Authorization header for internal auth."""
    return {"Authorization": f"Internal {TEST_INTERNAL_SECRET}"}


@pytest.fixture
def invalid_internal_auth_header() -> dict[str, str]:
    """Invalid Authorization header for internal auth."""
    return {"Authorization": "Internal wrong-secret-999"}


# ---------------------------------------------------------------------------
# Sample data fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_run_request() -> dict[str, Any]:
    """Valid /run request body matching the component contract."""
    return {
        "input": {"example_key": "example_value"},
        "callback_url": "https://api.example.com/v1/internal/jobs/123/complete",
    }
