# Cloud-Pilot Inventory

This project is complete locally. It measures a real local telemetry path: request →
trace/metrics → correlation → estimated cost and SLO result. It has not run on AWS.

## What an AWS pilot needs

- Private EKS workload for the demo producer and analytics API.
- RDS for durable correlation/audit state and S3 only if retained trace/artifact data needs it.
- OpenTelemetry Collector, Prometheus, Tempo, Grafana, Alertmanager, and a narrow ALB only for the API/dashboard if browser access is needed.
- ECR, IRSA, Secrets Manager, NetworkPolicies, non-root workloads, probes, limits, and PDBs.
- Terraform-only create/destroy, a separate state bucket/lock table, cost guardrail, GitHub OIDC, and recorded failure/load/teardown evidence.

## Current boundary

Terraform and AWS diagrams do not exist yet. They are the next staged work. No cloud,
GPU, managed-observability, billing, or production benchmark claim may be made until
an authorized pilot records evidence.
