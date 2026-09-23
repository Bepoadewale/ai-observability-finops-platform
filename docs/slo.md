# SLOs and error budgets

The illustrative local objective is **95% of successful requests with TTFT at or below one second**.
It is an example for the deterministic fixture, not a universal production target.

`GET /api/v1/slo?live_only=true` calculates compliance, bad-event count, event count, and remaining
error budget from persisted live usage metadata. A latency or saturation demo changes that result.
The primary request-analysis response includes the live SLO state alongside the request’s latency and
cost evidence.

Capacity advice is intentionally conservative: high average queueing produces `SATURATED` and a
recommendation to evaluate capacity or batching; the platform never makes an autonomous scaling or
cost-cutting action.
