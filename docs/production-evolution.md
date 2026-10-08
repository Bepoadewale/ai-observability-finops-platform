# Production Evolution

The local platform is complete. The cloud design now includes a private VPC/EKS/RDS/ECR
foundation, state guardrails, workload identity, secret boundaries, and secure workload
contracts. It is still not an AWS execution claim.

Before a cloud pilot can run, the service needs a PostgreSQL storage adapter, External
Secrets or an equivalent secret-delivery controller, immutable image publishing, EKS
bootstrap, and smoke/failure/teardown automation. These are the next delivery slices.

Do not claim real GPU cost, managed-observability behavior, cloud billing, or production
capacity until those measurements run in a named environment and are recorded.
