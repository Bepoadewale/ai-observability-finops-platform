#!/usr/bin/env bash
set -euo pipefail

# Future pilot drill: delete one API Pod and prove the deployment returns to two ready Pods.
# Run only in the named project namespace. This script does not grant cluster-admin access.
namespace="${AIOPS_NAMESPACE:-ai-observability}"
selector='app.kubernetes.io/name=analytics-api'

kubectl -n "$namespace" get deployment analytics-api
kubectl -n "$namespace" delete pod -l "$selector" --wait=false
kubectl -n "$namespace" rollout status deployment/analytics-api --timeout=180s
ready="$(kubectl -n "$namespace" get deployment analytics-api -o jsonpath='{.status.readyReplicas}')"
test "$ready" = "2"
echo "HA drill passed: analytics-api returned to 2 ready replicas."
