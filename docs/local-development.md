# Local development

## Prerequisites

- Docker Desktop running, including Docker Compose v2.
- Python 3.12 available as `python3.12`.
- `curl` and `jq` for the demo scripts.

No cloud account, GPU, model API key, Kubernetes cluster, or paid observability account is required.

## Start from a clean project state

```bash
make install
make bootstrap-local
make smoke
```

`bootstrap-local` builds the analytics and deterministic workload images, then starts the analytics
API, workload, OpenTelemetry Collector, Tempo, Prometheus, and Grafana. `smoke` uses bounded health
checks; it does not rely on arbitrary startup sleeps.

## Validate the full local story

```bash
make demo-local
make demo-degradation
make demo-cost-spike
make demo-tool-bottleneck
make demo-saturation
make demo-dashboard
make demo-recovery
make verify
```

See `docs/demo.md` for what each command asserts. Use `docker compose ps` and `docker compose logs`
when a dependency does not become ready.

## Safe cleanup

```bash
make clean-local
```

The target runs `docker compose down -v` for this repository’s Compose project and removes this
repository’s `.venv` and `.local` paths. It does not call global Docker prune commands and does not
delete other Docker workloads, clusters, images, or volumes.
