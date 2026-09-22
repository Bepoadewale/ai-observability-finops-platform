#!/usr/bin/env bash
set -euo pipefail

response=$(curl -fsS http://127.0.0.1:8081/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{"tenant_id":"team-payments","model":"llama-small","prompt":"investigate delayed payment","scenario":"latency"}')
request_id=$(printf '%s' "$response" | jq -r '.telemetry.request_id')
analysis=$(curl -fsS "http://127.0.0.1:8080/api/v1/requests/$request_id/analysis" \
  -H 'Authorization: Bearer tenant-payments')
printf '%s' "$analysis" | jq -e '.diagnostic_hints[] | select(contains("TTFT exceeds"))' >/dev/null
printf '%s' "$analysis" | jq -e '.diagnostic_hints[] | select(contains("Queueing is a material"))' >/dev/null
echo "degradation demo passed: request_id=$request_id"
