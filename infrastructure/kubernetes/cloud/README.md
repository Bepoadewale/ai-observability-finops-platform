# Cloud Workload Security Contract

These files describe how the future EKS workload will be constrained. They are not
deployed by this repository yet. The current analytics API stores metadata in SQLite,
so a PostgreSQL storage adapter is still required before a cloud apply can be called a
working durable runtime.

The contract requires a dedicated namespace and service account, workload identity,
non-root containers, read-only filesystems, dropped Linux capabilities, resource
limits, health probes, a disruption budget, and default-deny NetworkPolicies. Secrets
are referenced by name only. Secret values must come from AWS Secrets Manager through
External Secrets or an equivalent controller; they must never be committed, baked into
an image, or sent to browser code.
