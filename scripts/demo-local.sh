#!/usr/bin/env bash
set -euo pipefail

response=$(curl -fsS http://127.0.0.1:8081/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{"tenant_id":"team-search","model":"llama-small","prompt":"summarize safe platform controls","scenario":"normal"}')
request_id=$(printf '%s' "$response" | jq -r '.telemetry.request_id')
trace_id=$(printf '%s' "$response" | jq -r '.telemetry.trace_id')

analysis=$(curl -fsS "http://127.0.0.1:8080/api/v1/requests/$request_id/analysis" \
  -H 'Authorization: Bearer tenant-search')
test "$(printf '%s' "$analysis" | jq -r '.request_id')" = "$request_id"
test "$(printf '%s' "$analysis" | jq -r '.trace_id')" = "$trace_id"
test "$(printf '%s' "$analysis" | jq -r '.usage.model')" = "llama-small"

for _ in $(seq 1 20); do
  metrics=$(curl -fsS 'http://127.0.0.1:9090/api/v1/query?query=ai_requests_total' || true)
  if printf '%s' "$metrics" | jq -e '.data.result | length > 0' >/dev/null; then
    break
  fi
  sleep 1
done
printf '%s' "$metrics" | jq -e '.data.result | length > 0' >/dev/null

for _ in $(seq 1 20); do
  trace=$(curl -fsS "http://127.0.0.1:3200/api/traces/$trace_id" 2>/dev/null || true)
  if printf '%s' "$trace" | jq -e '.batches | length > 0' >/dev/null 2>&1; then
    break
  fi
  sleep 1
done
printf '%s' "$trace" | jq -e '.batches | length > 0' >/dev/null

echo "local demo passed: request_id=$request_id trace_id=$trace_id"
