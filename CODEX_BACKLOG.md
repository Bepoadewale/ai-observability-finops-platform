# P0 — Required for Portfolio Claim

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
