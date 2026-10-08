# Definition of Done

## Cloud-Pilot Readiness Gate

Cloud readiness requires a plain-English cloud story, icon-based architecture, separate Terraform state/lock/budget design, private runtime/security boundaries, delivery, observability/failure design, OIDC CI controls, and an exact evidence/teardown runbook. None of these count as AWS execution until a guarded Terraform create → validate → destroy pilot is recorded.

- [x] Cloud inventory identifies the local proof and cloud gaps.
- [x] Plain-English cloud story, temporary SVG/source/attribution, trust boundary, and operations/evolution docs are reviewed.
- [x] Separate state/lock/budget and private VPC/EKS/ECR/RDS/S3 Terraform contracts validate statically.
- [x] Static workload contracts define IRSA, secret references, non-root security, probes, limits, PDB, and default-deny network policy.
- [x] Static delivery contracts define immutable ECR images, Argo CD ownership, External Secrets references, and a narrow internal ALB route.
- [x] Static observability/reliability contracts define sanitized telemetry, alert rules, Pod-loss/bad-image recovery drills, bounded load, and cost-query design.
- [x] Static CI/CD and operations contracts define strict cloud validation, confirmation-gated GitHub OIDC plan/apply/destroy, and project-scoped operator commands.
- [ ] Replace the temporary primary architecture diagram with official AWS Architecture Icons before the cloud design gate is review-ready.
- [ ] Implement and execute PostgreSQL storage, secret delivery, EKS/GitOps runtime, observability, failure, and teardown proof before claiming cloud-pilot execution.

# Portfolio Complete — Local-First Scope Gate

- [x] A working local AI application/runtime generates real OTLP traces and Prometheus metrics.
- [x] OTel Collector, Prometheus, Tempo, and Grafana run locally and display generated data.
- [x] A request ID correlates trace, latency, tokens, queue/tool signal, model, cost, and SLO state.
- [x] Pricing is versioned and Decimal-safe; request, tenant, model, and workflow unit economics run on actual local telemetry.
- [x] Generated data changes SLO/error-budget computation.
- [x] Deterministic anomaly, what-if, capacity, and cost-optimization analysis execute on persisted live telemetry.
- [x] Normal, latency degradation, cost spike, tool bottleneck, and capacity saturation scenarios execute.
- [x] Telemetry state survives analytics API restart and duplicate ingestion is idempotent.
- [x] Reproducible demo, relevant unit/integration/E2E/failure tests, and CI workflow are configured.
- [x] GPU signals are labeled simulated; README/status reconcile every evidence boundary.

## Maturity Levels

- **FOUNDATION:** core architecture/logic exists.
- **PARTIALLY VALIDATED:** important analytics or integrations run but the central story is incomplete.
- **LOCAL END-TO-END VALIDATED:** successful local trace path runs with material failure/observability gaps.
- **PORTFOLIO COMPLETE — LOCAL-FIRST SCOPE:** every checked gate has executed evidence.

# Clean-Room Reproducibility Gate

`PORTFOLIO COMPLETE — LOCAL-FIRST SCOPE` requires two executed clean-room cycles: clone → install
→ bootstrap demo AI app, generator, OTel, Prometheus, tracing, Grafana → smoke →
telemetry/cost/SLO correlation demo → degradation/cost/security scenario → validation →
project-scoped cleanup → second clean bootstrap/demo.

- [x] Clean bootstrap had no hidden project state; primary and failure demos passed.
- [x] Cleanup removed only project resources; an unrelated Docker sentinel survived.
- [x] Post-cleanup absence and second bootstrap/demo are recorded in `docs/VALIDATION.md`.
