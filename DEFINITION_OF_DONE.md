# Definition of Done

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
