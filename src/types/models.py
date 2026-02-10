from typing import Any

from pydantic import BaseModel


class RunRequest(BaseModel):
    input: dict[str, Any] | None = None
    callback_url: str | None = None
    metadata: dict[str, Any] | None = None


class RunResponse(BaseModel):
    run_id: str
    status: str
    message: str | None = None


class HealthResponse(BaseModel):
    status: str


class UsageMetricsResponse(BaseModel):
    input_tokens: int
    output_tokens: int
    total_cost_usd: float
    api_calls: int
    started_at: str
    completed_at: str | None = None
