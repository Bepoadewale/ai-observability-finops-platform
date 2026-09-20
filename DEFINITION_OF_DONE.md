# Definition of Done

# Portfolio Complete — Local-First Scope Gate

- [ ] A working local AI application/runtime generates real OTLP traces and Prometheus metrics.
- [ ] OTel Collector, Prometheus, Tempo or chosen trace backend, and Grafana run locally and display generated data.
- [ ] A request ID correlates trace, latency, tokens, queue/tool/runtime signal, model, cost, and SLO state.
- [ ] Pricing is versioned and Decimal-safe; request, tenant, model, and claimed workflow unit economics run on actual local telemetry.
- [ ] Generated data changes SLO/error-budget computation.
- [ ] Deterministic anomaly, what-if, capacity, and cost-optimization analysis execute on real telemetry or explicitly separated simulated infrastructure signals.
- [ ] Normal, latency degradation, cost spike, tool bottleneck, and capacity saturation scenarios are executed where claimed.
- [ ] Reproducible demo, relevant unit/integration/E2E/failure tests, and CI are green.
- [ ] GPU signals are labeled simulated unless actual hardware is measured; README/status reconcile every evidence boundary.

## Maturity Levels

- **FOUNDATION:** core architecture/logic exists.
- **PARTIALLY VALIDATED:** important analytics or integrations run but the central story is incomplete.
- **LOCAL END-TO-END VALIDATED:** successful local trace path runs with material failure/observability gaps.
- **PORTFOLIO COMPLETE — LOCAL-FIRST SCOPE:** every checked gate has executed evidence.
