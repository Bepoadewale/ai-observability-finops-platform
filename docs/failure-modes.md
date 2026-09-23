# Failure modes

| Failure | Executed behavior / boundary |
| --- | --- |
| Analytics API restart | Live metadata remains in the project SQLite volume; `make demo-recovery` proves request analysis still works. |
| Duplicate usage event | `event_id` insertion is idempotent; duplicate ingestion returns `accepted: false`. |
| Slow request / queueing | The degradation and saturation demos report TTFT and queue evidence; no autoscaling occurs. |
| Tool latency | The tool-bottleneck demo attributes delay to tool execution rather than model latency. |
| Unknown price | Cost processing returns `PRICE_UNKNOWN`; it never silently uses zero. |
| Collector, trace, or scrape outage | The workload exposes an ingestion-failure metric and does not persist raw payloads. Durable retry/outbox delivery is a production-hardening gap. |

Partial traces do not invent missing cost. Monitor collector drops, exporter failures, scrape
failures, and cost-processing lag in a production adapter.
