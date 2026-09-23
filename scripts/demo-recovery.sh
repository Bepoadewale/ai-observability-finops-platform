#!/usr/bin/env bash
set -euo pipefail

response=$(curl -fsS http://127.0.0.1:8081/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{"tenant_id":"team-search","model":"llama-small","prompt":"verify telemetry durability","scenario":"normal"}')
request_id=$(printf '%s' "$response" | jq -r '.telemetry.request_id')

docker compose restart analytics-api >/dev/null
for _ in $(seq 1 30); do
  if curl -fsS http://127.0.0.1:8080/healthz >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

analysis=$(curl -fsS "http://127.0.0.1:8080/api/v1/requests/$request_id/analysis" \
  -H 'Authorization: Bearer tenant-search')
test "$(printf '%s' "$analysis" | jq -r '.classification.telemetry')" = "live metadata-only telemetry"
echo "recovery demo passed: request_id=$request_id persisted across analytics-api restart"
