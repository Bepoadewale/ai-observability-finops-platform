# Cloud Observability and Reliability Design

This page describes the future pilot checks. It does not claim that these checks have
run in AWS.

## What operators will see

The planned private observability stack receives sanitized OpenTelemetry traces, Prometheus
metrics, and Grafana dashboards. The same safe metadata used locally is the limit: no
raw prompts, completions, secret values, or browser credentials belong in traces, metrics,
or cost records.

The cloud contract defines two initial alerts:

- **high time to first token (TTFT):** the 95th percentile is above one second for ten
  minutes; and
- **missing telemetry target:** the expected demo AI metrics target is absent for five
  minutes.

The one-second value is an illustrative fixture objective, not a production SLO claim.
A future pilot must choose a product SLO, alert receiver, time window, and escalation
owner before treating an alert as an operational commitment.

## Availability and recovery drills

The analytics API contract starts with two replicas and a Pod Disruption Budget that keeps
one available during voluntary disruption. A future drill deletes one API Pod and waits
for Kubernetes to restore two ready replicas within a bounded timeout. The planned command
is `scripts/cloud-verify-ha.sh`; it has not run against EKS.

A separate failure drill will deliberately use a bad immutable image digest. The expected
result is failed readiness, not a false Ready state. Recovery is a reviewed Git revert to
the previously working digest followed by Argo CD reconciliation. The API does not run
`kubectl` itself.

## Bounded load and cost evidence

`infrastructure/load/cloud-bounded-load.js` is a two-virtual-user, two-minute k6 smoke
sample. It is deliberately small: it checks basic availability and latency without
pretending to be a sustained capacity or error-budget test.

`scripts/cloud-cost-evidence.sh` is a read-only Cost Explorer query grouped by the project
tag. AWS billing values can take 24–48 hours to settle. A future validation record must
label early values estimated or incomplete and must not claim measured savings from this
design.

## What still needs execution

A real pilot must start the private OTel Collector, Prometheus, Tempo, Grafana, and
Alertmanager; generate authenticated traffic; show a trace, dashboard, and firing alert;
run the Pod-loss and bad-image drills; run the bounded load sample; record the Cost
Explorer result; and destroy the pilot through Terraform.
