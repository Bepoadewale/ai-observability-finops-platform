# Cardinality

Do not label Prometheus metrics with request IDs, trace IDs, users, prompts or sessions. Those identifiers belong in traces or logs. Bounded labels such as model, deployment, tenant tier and outcome support aggregation without destabilizing the metrics backend.
