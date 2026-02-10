from abc import ABC, abstractmethod
from typing import Any


class Pipeline(ABC):
    """Abstract pipeline interface for component processing."""

    @abstractmethod
    async def execute(self, input: dict[str, Any], correlation_id: str) -> dict[str, Any]:
        """Execute the pipeline with the given input.

        Args:
            input: Pipeline input data.
            correlation_id: Request correlation ID for tracing.

        Returns:
            Pipeline output data.
        """
        ...

    @abstractmethod
    async def validate_input(self, input: dict[str, Any]) -> None:
        """Validate pipeline input before execution.

        Raises:
            ValidationError: If input is invalid.
        """
        ...
