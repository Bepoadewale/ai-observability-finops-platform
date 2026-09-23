# AI Observability + FinOps Platform — Agent Guide

Mission: correlate real local AI telemetry, reliability signals and cost estimates without collecting raw prompt data.

Stack: Python 3.12, FastAPI, OTel Collector, Prometheus, Tempo, Grafana, Docker Compose.

Commands: `make install`, `make bootstrap-local`, `make smoke`, `make demo-local`,
`make demo-degradation`, `make demo-cost-spike`, `make demo-tool-bottleneck`,
`make demo-saturation`, `make demo-dashboard`, `make demo-recovery`, `make verify`, and
`make clean-local`. Use `docker compose ps/logs` for stack proof.

Rules: label synthetic GPU data simulated; distinguish measured, estimated and forecast cost; never fabricate dashboards/telemetry; no secrets/main pushes; update status/backlog after validation.

Completion rule: do not mark **PORTFOLIO COMPLETE — LOCAL-FIRST SCOPE** unless `DEFINITION_OF_DONE.md` has executed evidence. Analytics code, fixture telemetry, Compose manifests, mocked tests, and dashboards without live data are insufficient. The AI request → telemetry → correlation → cost/SLO story must run locally; cloud/GPU adapters remain explicit.

## Clean-room reproducibility

Clean-room reproducibility is a mandatory completion criterion. Do not mark this repository
`PORTFOLIO COMPLETE — LOCAL-FIRST SCOPE` until a new engineer can reproduce the platform from a
clean project state using documented commands, execute the primary and required failure demos, run
validation, and safely tear down only this project's local resources. Do not infer reproducibility
from an existing developer environment; execute it after project-specific cleanup.
