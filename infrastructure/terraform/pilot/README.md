# Future FinOps Cloud Pilot

This root describes the future private AWS runtime. It has not been applied.

It plans a private VPC, private EKS control plane and workers, immutable ECR repository,
private RDS PostgreSQL state, encrypted evidence bucket, runtime secret container, and a
narrow IAM role for the analytics API. It does not open Prometheus, Tempo, Grafana,
PostgreSQL, Kubernetes, or Secrets Manager to the internet.

Before any future plan, create the separate state bucket and lock table through
`../bootstrap`, configure the S3 backend, provide a non-committed `terraform.tfvars`, and
review the account guardrail and every proposed resource. A Terraform plan is not AWS
execution evidence.
