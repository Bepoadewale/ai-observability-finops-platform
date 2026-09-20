# Completion Target

PORTFOLIO COMPLETE — LOCAL-FIRST SCOPE

# Current Completion Blockers

- Run a telemetry producer and local OTel/Prometheus/Tempo/Grafana stack with real data.
- Demonstrate request correlation, cost/SLO impact, and normal/degraded/cost/tool/capacity scenarios.

# P0 — Required for Portfolio Claim

P0 blocks PORTFOLIO COMPLETE — LOCAL-FIRST SCOPE; do not select P1/P2 work first.

- Build a lightweight local AI telemetry generator/runtime.
- Emit OTLP traces and Prometheus metrics through the collector.
- Start Compose and prove Prometheus/Tempo/Grafana receive generated data.
- Correlate request ID, latency, tokens, model, queue/tool signal, cost and SLO in API output.
- Exercise normal, latency, tool bottleneck, cost spike and saturation scenarios.

# P1 — Production Hardening

- Storage/replay, alert tests, dashboard tests and attribution quality controls.

# P2 — Enhancements

- Capacity what-if UI and expanded chargeback exports.

# P3 — Future / Cloud / Hardware

- GPU/DCGM and production observability providers.
# Clean-Room Completion Blocker

- [ ] Pass the full clean-room reproducibility gate: deterministic bootstrap, smoke, telemetry and degradation demos, safe cleanup, a second clean bootstrap, and recorded evidence. Break this into focused P0 work only during the scheduled week.
