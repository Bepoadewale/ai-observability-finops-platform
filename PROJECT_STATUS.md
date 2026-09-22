# Project Status

## Current Maturity

PARTIALLY VALIDATED

## Maturity Model

`FOUNDATION` → `PARTIALLY VALIDATED` → `LOCAL END-TO-END VALIDATED` → `PORTFOLIO COMPLETE — LOCAL-FIRST SCOPE`.

## Executed and Verified

- Analytics API, deterministic telemetry analysis, Decimal cost and SLO logic tests.
- Local Docker Compose execution: deterministic AI workload fixture → metadata-only analytics ingest
  → OTel Collector → Tempo trace and Prometheus metrics → request-level API correlation.
- `make demo-local` verified request ID and trace ID correlation with model, tokens, latency,
  queue/tool timing, and estimated/simulated cost. `make demo-degradation` generated latency and
  queue evidence with diagnosis hints.

## Implemented but Not End-to-End Validated

- Grafana dashboard starts from provisioned local configuration but does not yet render useful
  generated-data panels.
- Durable telemetry storage/replay and request-to-trace UI links.

## Simulated

- Golden telemetry and GPU pricing/data.

## Architecture / Contracts Only

- Production telemetry collectors, durable warehouse, and external runtime adapters.

## Known Failures

- GitHub CI rerun pending after adding explicit Python package discovery for the analytics source tree.

## Current P0 Objective

Turn the executed telemetry path into a complete diagnosis demo: durable live events, explicit SLO
impact, Grafana panels, and normal/degraded/cost/tool/capacity scenarios.

## Completion Blockers

- Grafana panels have not yet been proven with generated data.
- Live telemetry is in-memory only; persistence/recovery is unvalidated.
- Generated-data SLO/error-budget impact and FinOps unit economics need explicit demonstrations.
- Cost spike, tool bottleneck, and capacity saturation scenarios remain unexecuted.

## Explicitly Unexecuted Production Adapters

- Real GPU/DCGM hardware signals and production observability providers.

## Last Validation

- `make lint`: passed.
- `make test`: 5 passed (2 upstream TestClient deprecation warnings).
- `make smoke`: analytics API, demo workload, Prometheus, Tempo, and Grafana became ready.
- `make demo-local`: passed with real local metric, OTLP trace, analytics ingestion, and correlated request analysis.
- `make demo-degradation`: passed with real generated latency/queue telemetry and diagnosis hints.

## Last Updated

2026-09-22, live telemetry vertical slice in progress on `codex/week-06-ai-observability-finops`.

## Clean-Room Reproducibility

**Status: NOT YET VALIDATED**

Completion requires two executed clean-room cycles: clean start → bootstrap → smoke → primary demo
→ failure/security demo → validation → project-scoped cleanup, followed by a second clean bootstrap
and demo. Existing developer state is not evidence. This status must be `VALIDATED` before
`PORTFOLIO COMPLETE — LOCAL-FIRST SCOPE` is allowed.
