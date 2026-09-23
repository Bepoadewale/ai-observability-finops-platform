#!/usr/bin/env bash
set -euo pipefail

for _ in $(seq 1 30); do
  dashboard=$(curl -fsS -u admin:admin 'http://127.0.0.1:3000/api/dashboards/uid/ai-platform-health-local' || true)
  if printf '%s' "$dashboard" | jq -e '.dashboard.panels | length >= 5' >/dev/null 2>&1; then
    break
  fi
  sleep 1
done
printf '%s' "$dashboard" | jq -e '.dashboard.panels[] | select(.title == "Requests by tenant")' >/dev/null

metrics=$(curl -fsS --get 'http://127.0.0.1:9090/api/v1/query' --data-urlencode 'query=sum(ai_requests_total)')
printf '%s' "$metrics" | jq -e '.data.result[0].value[1] | tonumber > 0' >/dev/null
echo "dashboard demo passed: provisioned Grafana dashboard and generated Prometheus data are available"
