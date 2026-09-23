# Validation

## Clean-Room Validation

**Date:** 2026-09-23

**Implementation commit under test:** `1ccbebd`

**Environment:** macOS on Apple Silicon, Python 3.12, Docker Desktop with Docker Compose v2.
**Local services:** analytics API, deterministic AI workload fixture, OpenTelemetry Collector 0.134.1,
Tempo 2.8.2, Prometheus 3.5.0, and Grafana 12.1.0.

### Clean start and first cycle

Starting state was established with `make clean-local`. An unrelated container named
`aiops-unrelated-sentinel` was checked after cleanup to ensure project teardown did not delete
unrelated Docker resources.

```text
make install
make bootstrap-local
make smoke
make demo-local
make demo-degradation
make demo-cost-spike
make demo-tool-bottleneck
make demo-saturation
make demo-dashboard
make demo-recovery
make verify
make clean-local
```

Results: all services became ready; a request ID was found in Tempo and its metrics in Prometheus;
Grafana’s provisioned dashboard and generated metrics were queried through their APIs; the four
failure/diagnostic scenarios passed; and live metadata-only usage survived analytics API restart.
`make verify` passed: Ruff and 7 pytest tests passed (one upstream `TestClient` deprecation warning),
and `docker compose config --quiet` passed.

Post-cleanup verification found no running Compose service and no
`ai-observability-finops-platform_*` volume. The unrelated sentinel remained running.

### Second clean bootstrap

From that cleaned project state:

```text
make install
make bootstrap-local
make smoke
make demo-local
make demo-degradation
make verify
```

Results: the second bootstrap succeeded, all services reached readiness, primary trace/metric/cost
correlation and degradation diagnosis passed again, and validation passed. The unrelated sentinel
still survived, confirming cleanup scope.

## Evidence boundaries

The emitted traces and Prometheus metrics are real local telemetry. The AI workload is deterministic;
versioned token price calculations are estimates; GPU-time cost is simulated. No cloud billing,
production model performance, GPU utilization, or managed observability behavior was claimed.
