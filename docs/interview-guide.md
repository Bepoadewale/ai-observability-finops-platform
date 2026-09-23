# Interview guide

## Why this exists

AI observability is not only tracing. A useful platform connects a request to model/token use,
latency phases, queue/tool delays, reliability objective, tenant attribution, and cost while avoiding
raw prompt collection by default.

## What is measured here

The local workload emits real OTLP traces and Prometheus metrics. A request ID joins Tempo evidence,
Prometheus aggregates, a metadata-only SQLite event, estimated token price, simulated GPU-time cost,
and SLO state. The project demonstrates a realistic control loop, not a production GPU benchmark.

## Useful discussion points

- **TTFT vs TPOT:** TTFT describes initial responsiveness; TPOT describes decode smoothness. E2E
  duration alone hides queue and tool bottlenecks.
- **FinOps:** provider-style token cost and self-hosted allocation are different. Prices need source,
  version, effective date, and decimal arithmetic. A simulated GPU component is never an invoice.
- **SLO decisions:** queueing and bad TTFT can justify investigation, capacity evaluation, or
  batching—not blind capacity reduction or automatic action.
- **Privacy:** request/trace IDs enable correlation without placing prompts or completions into
  metrics labels or default telemetry.
- **Reliability:** ingestion is idempotent and survives API restart locally. Durable retry/outbox,
  retention, and warehouse delivery are explicitly future hardening work.
