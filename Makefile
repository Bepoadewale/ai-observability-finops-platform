PYTHON ?= python3.12
VENV := .venv
PY := $(VENV)/bin/python
export PYTHONPATH := analytics-api/src

.PHONY: install test lint demo bootstrap bootstrap-local smoke demo-local demo-degradation demo-recovery demo-cost-spike demo-tool-bottleneck demo-saturation demo-dashboard verify clean clean-local
install:
	command -v $(PYTHON) >/dev/null || { echo "Python 3.12 is required"; exit 1; }
	@if [ -x "$(PY)" ] && ! $(PY) -c 'import sys; assert sys.version_info[:2] == (3, 12)' >/dev/null 2>&1; then \
		echo "Recreating project-local virtual environment with Python 3.12"; rm -rf $(VENV); \
	fi
	$(PYTHON) -m venv $(VENV)
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -e '.[dev]'
test:
	$(PY) -m pytest -q
lint:
	$(PY) -m ruff check analytics-api/src tests scripts
demo:
	PYTHONPATH=analytics-api/src $(PY) -m uvicorn aiops.main:app --port 8080
bootstrap:
	docker compose up -d prometheus tempo grafana otel-collector
bootstrap-local: install
	docker compose up -d --build
smoke:
	./scripts/smoke.sh
demo-local:
	./scripts/demo-local.sh
demo-degradation:
	./scripts/demo-degradation.sh
demo-recovery:
	./scripts/demo-recovery.sh
demo-cost-spike:
	./scripts/demo-cost-spike.sh
demo-tool-bottleneck:
	./scripts/demo-tool-bottleneck.sh
demo-saturation:
	./scripts/demo-saturation.sh
demo-dashboard:
	./scripts/demo-dashboard.sh
verify:
	$(MAKE) lint
	$(MAKE) test
	docker compose config --quiet
clean:
	docker compose down -v
clean-local: clean
	rm -rf $(VENV) .local
