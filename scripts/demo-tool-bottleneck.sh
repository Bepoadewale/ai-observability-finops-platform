#!/usr/bin/env bash
set -euo pipefail

response=$(curl -fsS http://127.0.0.1:8081/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{"tenant_id":"team-payments","model":"llama-small","prompt":"check the payment provider status","scenario":"tool_bottleneck"}')
request_id=$(printf '%s' "$response" | jq -r '.telemetry.request_id')
analysis=$(curl -fsS "http://127.0.0.1:8080/api/v1/requests/$request_id/analysis" -H 'Authorization: Bearer tenant-payments')
recommendations=$(curl -fsS 'http://127.0.0.1:8080/api/v1/recommendations?live_only=true' -H 'Authorization: Bearer finops-demo')

printf '%s' "$analysis" | jq -e '.diagnostic_hints[] | select(contains("Tool execution dominates"))' >/dev/null
printf '%s' "$recommendations" | jq -e '.what_if | length == 1' >/dev/null
echo "tool bottleneck demo passed: request_id=$request_id identifies tool latency"
