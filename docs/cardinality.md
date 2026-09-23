# Cardinality

Prometheus labels are intentionally bounded:

- request counter: tenant and outcome;
- token counter and latency histograms: model/type;
- queue and tool histograms: deterministic scenario.

Request IDs, trace IDs, users, prompts, sessions, and arbitrary error payloads are never labels.
Request/trace IDs belong in the trace and the protected analytics API correlation path. This keeps
the local demonstration representative of a cardinality-safe measurement design.
