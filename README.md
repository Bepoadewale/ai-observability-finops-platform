# AI Observability + FinOps Platform

An independently runnable measurement and financial-control layer for AI systems. It correlates request performance, model token use, inferred queue/tool bottlenecks, SLO state, tenant attribution, and versioned-price cost estimates.

It complements the portfolio: Project 1 governs infrastructure, Project 2 serves models, Project 3 executes agents safely; this project measures reliability, efficiency, and economics across them.

## The local control loop

```text
deterministic AI workload
  → metadata-only usage ingestion (SQLite)
  → OpenTelemetry Collector → Tempo trace
  → Prometheus metrics → Grafana dashboard
  → tenant-scoped request analysis / FinOps / SLO APIs
```

The request body and response are deliberately excluded from traces, metrics, and stored usage.
The project uses a deterministic workload fixture to validate the platform path; it is not an ML
quality, production-capacity, GPU-performance, or cloud-cost benchmark.

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

## Local endpoints and demo identities

After `make bootstrap-local`, the local services are reachable at:

| Service | URL | Purpose |
| --- | --- | --- |
| Analytics API | `http://localhost:8080/docs` | request, cost, SLO, and recommendation APIs |
| Demo AI workload | `http://localhost:8081/docs` | deterministic OpenAI-shaped fixture endpoint |
| Prometheus | `http://localhost:9090` | generated metrics |
| Tempo | `http://localhost:3200` | trace query API |
| Grafana | `http://localhost:3000` | provisioned AI Platform dashboard |

The API uses intentionally non-secret local fixture tokens: `tenant-search`, `tenant-payments`,
`finops-demo`, and `telemetry-producer`. They demonstrate API scopes only and must never be used
outside local development.

On a pristine local bootstrap, Grafana uses its disposable `admin` / `admin` account and prompts for
a password change. `make demo-dashboard` verifies dashboard provisioning through Grafana's API with
that clean-bootstrap credential. If you change the password for an interactive session, reset the
project with `make clean-local` and `make bootstrap-local` before rerunning that scripted check.

## What the demos prove

- `demo-local`: real local request → OTLP trace, Prometheus metric, durable metadata-only usage,
  tenant-scoped analysis, estimated cost, and SLO result.
- `demo-degradation`: high TTFT and queueing produce diagnosis hints.
- `demo-tool-bottleneck`: tool duration is identified before blaming the model runtime.
- `demo-cost-spike`: high output tokens appear in request/workflow unit economics.
- `demo-saturation`: a bounded burst produces a capacity recommendation; it does not autoscale.
- `demo-recovery`: live metadata survives an analytics API restart.
- `demo-dashboard`: Grafana provisioning and generated Prometheus series are verified by API.

See [architecture](docs/architecture.md), [local development](docs/local-development.md),
[demo guide](docs/demo.md), [FinOps](docs/finops.md), [SLOs](docs/slo.md), and
[implementation status](docs/IMPLEMENTATION_STATUS.md).

## Classification

| Class | Meaning |
|---|---|
| measured | connected runtime telemetry |
| estimated | versioned price-catalog calculation |
| allocated | documented shared-cost split |
| forecast | scenario/run-rate output |
| simulated | local synthetic inference/GPU demo |

Raw prompts, completions, secrets and credentials are not recorded. See [architecture](docs/architecture.md), [FinOps](docs/finops.md), [SLOs](docs/slo.md), and [roadmap](docs/roadmap.md).
