PYTHON ?= python3
export PYTHONPATH := analytics-api/src

.PHONY: test lint demo bootstrap clean
test:
	$(PYTHON) -m pytest -q
lint:
	$(PYTHON) -m ruff check analytics-api/src tests
demo:
	$(PYTHON) -m uvicorn aiops.main:app --app-dir analytics-api/src --port 8080
bootstrap:
	docker compose up -d prometheus tempo grafana otel-collector
clean:
	docker compose down -v
