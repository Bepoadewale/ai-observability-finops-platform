# Roadmap and evidence boundary

## Executed locally

- Deterministic AI workload emitting real OTLP spans and Prometheus metrics.
- OpenTelemetry Collector → Tempo trace ingestion and Prometheus → Grafana dashboard path.
- Tenant-scoped request/cost/SLO analysis, versioned Decimal pricing, and metadata-only SQLite
  persistence with restart recovery.
- Normal, latency, tool-bottleneck, cost-spike, saturation, dashboard, and recovery demos.
- Two clean-room bootstrap/demo cycles with project-scoped cleanup.

## Production hardening

- Replace local opaque demo tokens with production identity, authorization, and audit controls.
- Use a managed durable store/warehouse with retention, replay, and data-quality controls.
- Add alert delivery, dashboard regression tests, and a production telemetry collection strategy.
- Integrate validated runtime, deployment, and provider-billing adapters.

## Unexecuted adapters

vLLM, DCGM, OpenCost, real GPUs, cloud invoices, managed observability, Kubernetes/EKS, and
production-scale retention are not validated here. Their architecture is deliberately separate from
the local completed control loop.
