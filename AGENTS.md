# AI Observability + FinOps Platform — Agent Guide

Mission: correlate real local AI telemetry, reliability signals and cost estimates without collecting raw prompt data.

Stack: Python 3.12, FastAPI, OTel Collector, Prometheus, Tempo, Grafana, Docker Compose.

Commands: `make test`, `make lint`, `make demo`, `make bootstrap`; use `docker compose ps/logs` for stack proof.

Rules: label synthetic GPU data simulated; distinguish measured, estimated and forecast cost; never fabricate dashboards/telemetry; no secrets/main pushes; update status/backlog after validation.
