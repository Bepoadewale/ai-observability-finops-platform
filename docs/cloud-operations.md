# Cloud Operations

The cloud pilot will be off by default because it creates billable AWS resources.
Terraform will be the only create/destroy mechanism. Before any apply, an operator
must review the account, region, tags, budget, and plan.

The pilot will record: a normal request, a latency/cost/failure scenario, metrics,
traces, dashboard evidence, alert evidence, a bounded load sample, an AWS cost query,
and Terraform teardown checks. Cost Explorer values remain estimates until AWS billing
settles, often 24–48 hours later.

## Before a future pilot

1. Create this repository's state bucket and lock table through the bootstrap Terraform
   root. Keep `terraform.tfvars` outside Git.
2. Run `make terraform-validate`. It validates the bootstrap and private-runtime
   Terraform contracts without creating AWS resources.
3. Review the account-ID check, tags, expected cost, RDS deletion protection, and the
   complete Terraform plan before any apply.
4. Do not apply the runtime contract until the PostgreSQL storage adapter, secret
   delivery controller, image publishing, and runtime bootstrap are implemented and
   tested.
