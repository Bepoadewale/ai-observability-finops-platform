#!/usr/bin/env bash
set -euo pipefail

command_name="${1:?Choose guardrails-plan, plan, apply, push-image, bootstrap-runtime, smoke, validate, or destroy.}"
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
terraform_root="$root/infrastructure/terraform"

require() {
  local variable="$1"
  [[ -n "${!variable:-}" ]] || { echo "$variable is required." >&2; exit 1; }
}

require_account() {
  require EXPECTED_AWS_ACCOUNT_ID
  local actual
  actual="$(aws sts get-caller-identity --query Account --output text)"
  [[ "$actual" == "$EXPECTED_AWS_ACCOUNT_ID" ]] || {
    echo "Wrong AWS account: expected $EXPECTED_AWS_ACCOUNT_ID, got $actual." >&2
    exit 1
  }
}

init_runtime_backend() {
  require TF_STATE_BUCKET
  require TF_LOCK_TABLE
  terraform -chdir="$terraform_root/pilot" init -reconfigure \
    -backend-config="bucket=$TF_STATE_BUCKET" \
    -backend-config="key=${TF_STATE_KEY:-pilot/runtime.tfstate}" \
    -backend-config="region=${AWS_REGION:-us-east-1}" \
    -backend-config="dynamodb_table=$TF_LOCK_TABLE" \
    -backend-config="encrypt=true"
}

pilot_vars=()
add_pilot_vars() {
  require EXPECTED_AWS_ACCOUNT_ID
  require BUDGET_ALERT_EMAIL
  pilot_vars=(
    "-var=expected_account_id=$EXPECTED_AWS_ACCOUNT_ID"
    "-var=budget_alert_email=$BUDGET_ALERT_EMAIL"
  )
}

case "$command_name" in
  guardrails-plan)
    require_account
    require BUDGET_ALERT_EMAIL
    terraform -chdir="$terraform_root/bootstrap" init -backend=false
    terraform -chdir="$terraform_root/bootstrap" plan \
      -var="expected_account_id=$EXPECTED_AWS_ACCOUNT_ID" \
      -var="budget_alert_email=$BUDGET_ALERT_EMAIL"
    ;;
  plan)
    require_account
    add_pilot_vars
    init_runtime_backend
    terraform -chdir="$terraform_root/pilot" plan "${pilot_vars[@]}"
    ;;
  apply)
    [[ "${CONFIRM_APPLY:-}" == "APPLY_FINOPS_PILOT" ]] || {
      echo "Set CONFIRM_APPLY=APPLY_FINOPS_PILOT after reviewing the exact plan." >&2; exit 1;
    }
    require_account
    add_pilot_vars
    init_runtime_backend
    terraform -chdir="$terraform_root/pilot" apply "${pilot_vars[@]}"
    ;;
  push-image)
    require ECR_REPOSITORY_URL
    require IMAGE_TAG
    require_account
    aws ecr get-login-password | docker login --username AWS --password-stdin "${ECR_REPOSITORY_URL%%/*}"
    docker build -t "$ECR_REPOSITORY_URL:$IMAGE_TAG" "$root"
    docker push "$ECR_REPOSITORY_URL:$IMAGE_TAG"
    echo "Image pushed. Record its digest before updating the GitOps manifest."
    ;;
  bootstrap-runtime)
    require KUBECONFIG
    command -v helm >/dev/null || { echo "helm is required." >&2; exit 1; }
    command -v kubectl >/dev/null || { echo "kubectl is required." >&2; exit 1; }
    echo "Preflight only: verify the private EKS connection, controller roles, External Secrets, Argo CD, and PostgreSQL migration before bootstrap."
    kubectl version --request-timeout=20s >/dev/null
    kubectl get namespace argocd --request-timeout=20s >/dev/null
    ;;
  smoke)
    require KUBECONFIG
    kubectl -n ai-observability rollout status deployment/analytics-api --timeout=180s
    kubectl -n ai-observability get pods -l app.kubernetes.io/name=analytics-api
    echo "Smoke preconditions passed. Run the authenticated trace, alert, and failure drills from docs/cloud-operations.md."
    ;;
  validate)
    "$root/scripts/validate-cloud-contracts.sh"
    ;;
  destroy)
    [[ "${CONFIRM_DESTROY:-}" == "DESTROY_FINOPS_PILOT" ]] || {
      echo "Set CONFIRM_DESTROY=DESTROY_FINOPS_PILOT after recording validation evidence." >&2; exit 1;
    }
    require_account
    add_pilot_vars
    init_runtime_backend
    terraform -chdir="$terraform_root/pilot" destroy \
      -var="rds_deletion_protection=false" \
      "${pilot_vars[@]}"
    ;;
  *)
    echo "Unknown command: $command_name" >&2
    exit 1
    ;;
esac
