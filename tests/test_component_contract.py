"""Component contract tests.

Every platform component MUST pass these tests. They verify the
component interface contract: /health and /run endpoints.
"""

import pytest


@pytest.mark.asyncio
async def test_health_returns_healthy(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_run_returns_202(client):
    response = await client.post("/run", json={"input": {"test": True}})
    assert response.status_code == 202
    data = response.json()
    assert "run_id" in data
    assert data["status"] == "accepted"


@pytest.mark.asyncio
async def test_run_without_input(client):
    response = await client.post("/run", json={})
    assert response.status_code == 202


@pytest.mark.asyncio
async def test_health_response_shape(client):
    response = await client.get("/health")
    data = response.json()
    assert set(data.keys()) == {"status"}


@pytest.mark.asyncio
async def test_run_response_shape(client):
    response = await client.post("/run", json={"input": {}})
    data = response.json()
    assert "run_id" in data
    assert "status" in data
