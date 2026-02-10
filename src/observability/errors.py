class ComponentError(Exception):
    """Base error for all component errors."""

    status_code: int = 500

    def __init__(self, detail: str = "Internal component error"):
        self.detail = detail
        super().__init__(detail)


class ValidationError(ComponentError):
    """Input validation failed."""

    status_code = 422


class PipelineError(ComponentError):
    """Pipeline execution failed."""

    status_code = 500


class DependencyError(ComponentError):
    """External dependency (database, API) unavailable."""

    status_code = 503


class ConfigurationError(ComponentError):
    """Missing or invalid configuration."""

    status_code = 500
