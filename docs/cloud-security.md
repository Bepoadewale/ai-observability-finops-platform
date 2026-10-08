# Cloud Security and State Design

This page describes the planned AWS security boundary. It is a design and Terraform
contract, not proof that AWS has run it.

## What stays private

The future analytics API, telemetry collector, Prometheus, Tempo, Grafana administration,
PostgreSQL, Kubernetes API, and secret store stay inside private network boundaries. A
future browser route, if needed, will expose only the exact dashboard or API path needed
for a user. It will not publish the database, observability administration, Kubernetes,
or secrets.

## Who can do what

| Actor | Allowed | Not allowed |
| --- | --- | --- |
| Analytics API Pod | Read its named runtime secret and read/write the named evidence bucket through its own IAM role | AWS administrator access, wildcard secret access, or a developer's AWS credentials |
| Telemetry producer | Send metadata-only telemetry to the API/collector | Send raw prompts or browse the database |
| Platform operator | Review a Terraform plan and approve a future apply/destroy | Put long-lived AWS keys in GitHub or bypass the account guardrail |
| Browser user | View only the future narrow user route after trusted sign-in | Reach PostgreSQL, Prometheus, Tempo, Grafana administration, or Kubernetes directly |

## State and secrets

The local SQLite database is useful for the local demo only. The future cloud storage
design uses private, encrypted RDS PostgreSQL for durable correlation and cost state.
The current Python storage adapter does not yet speak PostgreSQL. That migration is a
required cloud-pilot implementation task; an RDS resource in Terraform is not a claim
that the running application already uses it.

Terraform creates a Secrets Manager container, not secret values. A future External
Secrets controller will copy only the required named value into the workload namespace.
Values must never be placed in Git, Docker images, Terraform variables committed to the
repository, logs, metrics, traces, or browser JavaScript.

## Workload protection

The checked-in Kubernetes contract requires:

- a dedicated namespace and service account;
- IAM Roles for Service Accounts (IRSA), so the Pod receives a narrow AWS role instead
  of node-wide credentials;
- non-root execution, no privilege escalation, dropped Linux capabilities, read-only
  root filesystem, and the Kubernetes default seccomp profile;
- CPU/memory requests and limits, health probes, two replicas, and a disruption budget;
- default-deny ingress and egress NetworkPolicies, opened only for required paths.

These controls are statically checked in `tests/test_cloud_contracts.py`. They still
need a real EKS pilot before they count as executed security evidence.

## Terraform safety

Each future pilot must use the repository's own encrypted, versioned state bucket and
DynamoDB lock table. Terraform checks the intended account ID before a plan or apply.
All resources carry project and environment tags. The RDS design enables encryption,
backups, deletion protection, and a final snapshot. An operator must intentionally
change the deletion guard before a future Terraform destroy.
