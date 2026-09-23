# OpenTelemetry GenAI

The local workload creates a `gen_ai.inference` span and records bounded operational attributes:
request ID, tenant, model, input/output token counts, scenario, and whether telemetry ingestion
succeeded. It does not record prompt or response content.

The workload emits OTLP/HTTP to the local OpenTelemetry Collector, which exports traces to Tempo.
`make demo-local` waits for the trace to be queryable by its generated trace ID. Production adapters
should follow the current GenAI semantic conventions, propagate W3C context across tool calls, and
review tenant/cardinality attributes before rollout.
