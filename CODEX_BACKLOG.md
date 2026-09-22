# Completion Target

PORTFOLIO COMPLETE — LOCAL-FIRST SCOPE

# Current Completion Blockers

- Complete durable telemetry storage/recovery, generated-data SLO/cost evidence, Grafana panels,
  and the remaining required scenarios.

# P0 — Required for Portfolio Claim

P0 blocks PORTFOLIO COMPLETE — LOCAL-FIRST SCOPE; do not select P1/P2 work first.

- [x] Build a lightweight local AI telemetry generator/runtime.
- [x] Emit OTLP traces and Prometheus metrics through the collector.
- [x] Start Compose and prove Prometheus and Tempo receive generated data.
- [x] Correlate request ID, latency, tokens, model, queue/tool signal, and estimated cost in API output.
- [ ] Persist live telemetry and validate restart recovery without duplicate ingestion.
- [ ] Demonstrate generated-data SLO/error-budget change and unit-economics outputs.
- [ ] Render and verify Grafana panels from generated data.
- [ ] Exercise cost spike, tool bottleneck, and capacity saturation scenarios.

# P1 — Production Hardening

- Storage/replay, alert tests, dashboard tests and attribution quality controls.

# P2 — Enhancements

- Capacity what-if UI and expanded chargeback exports.

# P3 — Future / Cloud / Hardware

- GPU/DCGM and production observability providers.
# Clean-Room Completion Blocker

- [ ] Pass the full clean-room reproducibility gate: deterministic bootstrap, smoke, telemetry and degradation demos, safe cleanup, a second clean bootstrap, and recorded evidence. Break this into focused P0 work only during the scheduled week.
