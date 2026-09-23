# Privacy

The executed local path deliberately excludes prompts, completions, source code, credentials, and
tool payloads from persisted usage, Prometheus labels, OTel attributes, and the analytics response.
Correlation uses request and trace IDs; those IDs are not Prometheus labels.

The stored `UsageEvent` contains operational metadata: tenant/team, model/deployment, token counts,
latency breakdown, success, and optional workflow ID. This is sufficient for the local FinOps/SLO
demonstration without collecting request content.

The local bearer tokens are non-secret fixtures. Production use needs real identity, tenant
authorization, retention policy, encryption, access audit, and an explicit content-capture policy.
