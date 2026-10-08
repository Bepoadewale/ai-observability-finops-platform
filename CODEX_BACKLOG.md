# Completion Target

PORTFOLIO COMPLETE — LOCAL-FIRST SCOPE

# Current Completion Blockers

None within local-first scope. Do not reopen a completion claim without new executed evidence.

# Cloud-Pilot Readiness

- [x] CP0: record cloud inventory and evidence boundary.
- [ ] CP1: add plain-English cloud story, icon-based AWS architecture, trust boundary, and governance links.
- [ ] CP2–CP6: complete the staged cloud-pilot program; no AWS apply until separately authorized.

# P0 — Required for Portfolio Claim

P0 blocks `PORTFOLIO COMPLETE — LOCAL-FIRST SCOPE`; no P1/P2 work should be selected while a P0
blocker exists.

- [x] Build a lightweight local AI telemetry generator/runtime.
- [x] Emit OTLP traces and Prometheus metrics through the collector.
- [x] Start Compose and prove Prometheus and Tempo receive generated data.
- [x] Correlate request ID, latency, tokens, model, queue/tool signal, and estimated cost in API output.
- [x] Persist live telemetry and validate restart recovery without duplicate ingestion.
- [x] Demonstrate generated-data SLO/error-budget change and unit-economics outputs.
- [x] Render and verify Grafana panels from generated data.
- [x] Exercise cost spike, tool bottleneck, and capacity saturation scenarios.
- [x] Pass full clean-room reproducibility gate with safe cleanup and second bootstrap.

# P1 — Production Hardening

- Make Grafana dashboard validation accept an explicitly configured local API credential after an
  interactive user changes the disposable clean-bootstrap password.
- Add authenticated production identity and tenant-scoped durable storage migration strategy.
- Add alert delivery and dashboard regression tests.
- Add a supported production telemetry-warehouse adapter and retention controls.

# P2 — Enhancements

- Expand what-if and chargeback exports.

# P3 — Future / Cloud / Hardware

- Integrate real GPU/DCGM and managed-cloud observability providers.
