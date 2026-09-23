# High TTFT runbook

## Local investigation path

1. Run `make demo-degradation` and inspect the returned request ID.
2. Query `GET /api/v1/requests/{request_id}/analysis` with the matching tenant fixture token.
3. Confirm whether the diagnosis identifies queueing, TTFT, or tool duration.
4. Open the Grafana dashboard and compare TTFT/queue panels with the generated scenario.
5. Query Tempo using the correlated trace ID to inspect the `gen_ai.inference` span.

## Decision boundary

High queueing supports a recommendation to evaluate capacity or batching; it is not permission to
autoscale automatically. The local project does not measure KV cache pressure, physical GPU
utilization, network, or provider performance. Those are production-adapter inputs and must not be
inferred from this deterministic workload.
