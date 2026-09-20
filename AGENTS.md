# AI Observability + FinOps Platform — Agent Guide

Mission: correlate real local AI telemetry, reliability signals and cost estimates without collecting raw prompt data.

Stack: Python 3.12, FastAPI, OTel Collector, Prometheus, Tempo, Grafana, Docker Compose.

Commands: `make test`, `make lint`, `make demo`, `make bootstrap`; use `docker compose ps/logs` for stack proof.

Rules: label synthetic GPU data simulated; distinguish measured, estimated and forecast cost; never fabricate dashboards/telemetry; no secrets/main pushes; update status/backlog after validation.

Completion rule: do not mark **PORTFOLIO COMPLETE — LOCAL-FIRST SCOPE** unless `DEFINITION_OF_DONE.md` has executed evidence. Analytics code, fixture telemetry, Compose manifests, mocked tests, and dashboards without live data are insufficient. The AI request → telemetry → correlation → cost/SLO story must run locally; cloud/GPU adapters remain explicit.
