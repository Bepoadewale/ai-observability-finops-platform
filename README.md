# AI Observability + FinOps Platform

An independently runnable measurement and financial-control layer for AI systems. It correlates request performance, model token use, inferred queue/tool bottlenecks, SLO state, tenant attribution, and versioned-price cost estimates.

It complements the portfolio: Project 1 governs infrastructure, Project 2 serves models, Project 3 executes agents safely; this project measures reliability, efficiency, and economics across them.

## What is genuinely implemented

- FastAPI analytics API with tenant-scoped access, idempotent durable metadata-only ingestion,
  request-to-cost analysis, Decimal currency calculation, versioned pricing, SLO/error-budget
  calculation, unit economics, and deterministic diagnosis recommendations.
- Deterministic golden telemetry for two tenants, a tool-bound request, and a saturated deployment regression.
- A local deterministic AI-workload fixture that emits real OTLP traces and Prometheus metrics,
  forwards metadata-only usage to the analytics API, and supports normal and latency-degradation
  demonstrations through Docker Compose.
- Local Tempo, OpenTelemetry Collector, Prometheus, and Grafana with a generated-data dashboard.
- Synthetic GPU pricing/data design. It is always labeled simulated; no GPU claim is made.

## Local run

```bash
make install
make bootstrap-local
make smoke
make demo-local        # real local metric, trace, analytics ingest and correlated analysis
make demo-degradation  # latency/queue evidence with diagnosis hints
make demo-cost-spike
make demo-tool-bottleneck
make demo-saturation
make demo-dashboard
make demo-recovery     # persisted metadata remains correlated after API restart
make verify
make clean-local       # removes only this project's Compose resources and local state
```

The workload fixture is intentionally deterministic and is not a model-quality, GPU-performance,
or production-capacity claim. Raw prompts and responses are excluded from metrics, traces, and
analytics ingestion.

## Reproducibility

Two clean-room cycles have been executed from project-scoped cleanup. The first ran every primary,
failure, dashboard, recovery, and verification path; the second rebuilt and reran the core demo.
`make clean-local` uses Docker Compose project scope and removes the project’s local virtualenv and
state. It does not use global Docker prune commands. See [validation](docs/VALIDATION.md).

## Classification

| Class | Meaning |
|---|---|
| measured | connected runtime telemetry |
| estimated | versioned price-catalog calculation |
| allocated | documented shared-cost split |
| forecast | scenario/run-rate output |
| simulated | local synthetic inference/GPU demo |

Raw prompts, completions, secrets and credentials are not recorded. See [architecture](docs/architecture.md), [FinOps](docs/finops.md), [SLOs](docs/slo.md), and [roadmap](docs/roadmap.md).
