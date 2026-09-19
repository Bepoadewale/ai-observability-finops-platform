# Interview guide

Explain TTFT as prefill/user responsiveness and TPOT as decode smoothness; E2E alone hides queue and tool bottlenecks. Prometheus stores bounded aggregate metrics, Tempo stores request detail, and OpenTelemetry propagates context between application, inference and tools.

Provider cost is token-priced; self-hosted cost needs allocation of GPU time, utilization, idle capacity and shared overhead. FinOps cannot remove spare capacity without considering burst demand and SLO headroom. RED covers API rate/errors/duration; USE covers GPU/resource utilization, saturation and errors.
