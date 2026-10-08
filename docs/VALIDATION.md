# Validation

## Cloud-pilot baseline inventory

**Date:** 2026-10-08. `make install` then `make verify` passed: Ruff, 7 tests, and Compose configuration. No Docker stack, AWS credential, Terraform command, or cloud resource was used for this inventory.

## Cloud-story documentation review

**Date:** 2026-10-08. Cloud architecture, operations, and production-evolution documents
were added as design-only documentation. No AWS credential, Terraform command, cloud
resource, or cloud telemetry was used.

## Cloud security/state contract validation

**Date:** 2026-10-08. `terraform fmt -recursive infrastructure/terraform`,
`make terraform-validate`, `make cloud-contracts-validate`, and
`make kustomize-validate` passed. The complete Python test suite also passed: 13 tests,
with one upstream `TestClient` deprecation warning. These checks validate HCL and
checked-in workload and delivery contracts only. They did not authenticate to AWS, create
a resource, run a Terraform plan, or prove a cloud runtime.

## Cloud observability/reliability contract validation

**Date:** 2026-10-08. `make cloud-observability-contracts-validate` passed (8 static
contract tests). `make kustomize-validate`, `make terraform-validate`, `make lint`,
`make test` (15 passed, one upstream `TestClient` deprecation warning), and
`docker compose config --quiet` also passed. These checks validate the planned sanitized
telemetry, alerts, bounded load, failure recovery, and cost-evidence interfaces. No AWS
credentials, Cost Explorer query, Kubernetes cluster, load test, alert, or cloud telemetry
was used.

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
