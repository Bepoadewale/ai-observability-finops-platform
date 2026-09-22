# AI Observability + FinOps Platform

An independently runnable measurement and financial-control layer for AI systems. It correlates request performance, model token use, inferred queue/tool bottlenecks, SLO state, tenant attribution, and versioned-price cost estimates.

It complements the portfolio: Project 1 governs infrastructure, Project 2 serves models, Project 3 executes agents safely; this project measures reliability, efficiency, and economics across them.

## What is genuinely implemented

- FastAPI analytics API with tenant-scoped access, request-to-cost analysis, idempotent usage-ingestion primitives, Decimal currency calculation, versioned pricing, SLO/error-budget calculation, and SLO-aware capacity advice.
- Deterministic golden telemetry for two tenants, a tool-bound request, and a saturated deployment regression.
- A local deterministic AI-workload fixture that emits real OTLP traces and Prometheus metrics,
  forwards metadata-only usage to the analytics API, and supports normal and latency-degradation
  demonstrations through Docker Compose.
- Local Tempo, OpenTelemetry Collector, Prometheus, Grafana provisioning and alert/recording-rule examples.
- Synthetic GPU pricing/data design. It is always labeled simulated; no GPU claim is made.

## Local run

```bash
make install
make bootstrap-local
make smoke
make demo-local        # real local metric, trace, analytics ingest and correlated analysis
make demo-degradation  # latency/queue evidence with diagnosis hints
make verify
```

The workload fixture is intentionally deterministic and is not a model-quality, GPU-performance,
or production-capacity claim. Raw prompts and responses are excluded from metrics, traces, and
analytics ingestion.

## Classification

| Class | Meaning |
|---|---|
| measured | connected runtime telemetry |
| estimated | versioned price-catalog calculation |
| allocated | documented shared-cost split |
| forecast | scenario/run-rate output |
| simulated | local synthetic inference/GPU demo |

Raw prompts, completions, secrets and credentials are not recorded. See [architecture](docs/architecture.md), [FinOps](docs/finops.md), [SLOs](docs/slo.md), and [roadmap](docs/roadmap.md).
