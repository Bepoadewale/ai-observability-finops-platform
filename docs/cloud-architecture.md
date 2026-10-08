# Planned AWS Cloud Architecture

This is a design target, not AWS execution evidence.

![Planned AWS pilot](assets/finops-cloud-architecture.svg)

```text
AI workload → OpenTelemetry Collector → Tempo / Prometheus → Grafana
                     ↓
                Analytics API → RDS correlation and cost state
                     ↓
        private EKS · ECR · IAM/IRSA · Secrets Manager · S3 when needed
```

In plain English: the platform will collect safe request metadata, correlate it with
traces and metrics, calculate estimated cost, and show whether an SLO was met. The
workload, analytics API, and observability tools stay private. Terraform will manage
the VPC, EKS, storage, identity, and teardown. A narrow ALB is planned only if a
browser needs the dashboard/API; Prometheus, Tempo, Grafana administration, databases,
Kubernetes, and secrets will not be public.

The cloud pilot must prove the same story that already runs locally: request ID →
trace → metric → tenant/model/token metadata → cost/SLO explanation. GPU cost remains
simulated until real hardware telemetry is measured.

## Planned security and state boundary

Terraform now contains a static pilot contract for a private VPC, private EKS endpoint,
immutable ECR repository, encrypted RDS PostgreSQL, encrypted evidence bucket, Secrets
Manager container, and a narrow Pod IAM role. Kubernetes manifests describe two secured
analytics API replicas, a disruption budget, and default-deny network policies.

This is not a cloud execution claim. The current service still uses SQLite locally, so a
PostgreSQL storage adapter must be implemented before an AWS pilot can prove durable cloud
state. See [cloud security and state design](cloud-security.md).

## Planned delivery boundary

Terraform creates the private foundation; a reviewed Git change holds the workload state;
Argo CD is planned to reconcile that state into EKS. The planned ingress is internal and
routes only the analytics API paths. See [cloud delivery design](cloud-delivery.md).
