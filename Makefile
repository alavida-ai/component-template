.PHONY: dev test smoke clean format lint typecheck

dev:
	uv run uvicorn src.api.server:app --reload --host 0.0.0.0 --port 8000

test:
	uv run pytest tests/ -v

smoke:
	@echo "=== Smoke Test ==="
	@echo "1. Checking imports..."
	uv run python -c "from src.api.server import app; from src.types.models import RunRequest, RunResponse, HealthResponse; print('Imports OK')"
	@echo "2. Booting server..."
	uv run uvicorn src.api.server:app --host 0.0.0.0 --port 8000 & \
		SERVER_PID=$$!; \
		sleep 3; \
		echo "3. Checking /health..."; \
		curl -sf http://localhost:8000/health && echo "" && echo "Smoke test PASSED" || echo "Smoke test FAILED"; \
		kill $$SERVER_PID 2>/dev/null || true

format:
	uv run black src/ tests/

lint:
	uv run ruff check src/ tests/

typecheck:
	uv run mypy src/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf .ruff_cache htmlcov .coverage
