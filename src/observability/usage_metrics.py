from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class UsageMetrics:
    """Track token usage and costs for LLM-based pipelines."""

    input_tokens: int = 0
    output_tokens: int = 0
    total_cost_usd: float = 0.0
    api_calls: int = 0
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: datetime | None = None

    def record_call(self, input_tokens: int, output_tokens: int, cost_usd: float):
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.total_cost_usd += cost_usd
        self.api_calls += 1

    def complete(self):
        self.completed_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_cost_usd": round(self.total_cost_usd, 6),
            "api_calls": self.api_calls,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
