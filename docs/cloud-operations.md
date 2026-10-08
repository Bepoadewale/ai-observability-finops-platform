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

## Future delivery checks

Before an Argo CD sync, confirm the ECR image digest, workload IAM role, External Secrets
status, database migration, and health endpoint. Wait on each component's readiness
condition with a bounded timeout. Do not use fixed sleep commands or `kubectl apply` as a
replacement for the reviewed GitOps path.

## Future operator commands

These commands are present now so a future pilot has one predictable path. They refuse
to run in the wrong AWS account and apply/destroy require exact confirmation text. They
are unexecuted contracts, not proof that the pilot exists.

```bash
# Read-only planning. Set these values outside Git.
export AWS_PROFILE=<operator-profile>
export EXPECTED_AWS_ACCOUNT_ID=<account-id>
export TF_STATE_BUCKET=<this-repository-state-bucket>
export TF_LOCK_TABLE=<this-repository-lock-table>
export BUDGET_ALERT_EMAIL=<operator-email>

make pilot-guardrails-plan
make pilot-cloud-plan

# After a reviewed plan only.
CONFIRM_APPLY=APPLY_FINOPS_PILOT make pilot-cloud-apply
ECR_REPOSITORY_URL=<repository-url> IMAGE_TAG=<immutable-tag> make pilot-cloud-push-image
KUBECONFIG=<private-cluster-config> make pilot-cloud-bootstrap-runtime
KUBECONFIG=<private-cluster-config> make pilot-cloud-smoke

# Only after evidence is recorded and RDS deletion is deliberately reviewed.
CONFIRM_DESTROY=DESTROY_FINOPS_PILOT make pilot-cloud-destroy
```

`make pilot-cloud-validate` is safe to run without AWS credentials. It checks Terraform,
Kubernetes/Kustomize, and static cloud contracts.

## Future GitHub Actions setup

The `cloud-pilot` workflow uses GitHub OpenID Connect (OIDC), not stored AWS access keys.
Before it can run, create a restricted AWS role that trusts this repository, add its ARN
as `AWS_PILOT_OIDC_ROLE_ARN`, and add the expected account, region, state bucket, lock
table, and budget email as GitHub environment variables in the protected `aws-pilot`
environment. Require human reviewers for that environment. The workflow has plan, apply,
and destroy dropdown choices; apply and destroy also require their exact confirmation text.
