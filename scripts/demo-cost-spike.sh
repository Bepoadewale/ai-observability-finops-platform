#!/usr/bin/env bash
set -euo pipefail

response=$(curl -fsS http://127.0.0.1:8081/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{"tenant_id":"team-search","model":"llama-small","prompt":"summarize the monthly AI cost report","scenario":"cost_spike","agent_run_id":"workflow-cost-demo"}')
request_id=$(printf '%s' "$response" | jq -r '.telemetry.request_id')
analysis=$(curl -fsS "http://127.0.0.1:8080/api/v1/requests/$request_id/analysis" -H 'Authorization: Bearer tenant-search')
economics=$(curl -fsS 'http://127.0.0.1:8080/api/v1/unit-economics?live_only=true' -H 'Authorization: Bearer finops-demo')

test "$(printf '%s' "$analysis" | jq -r '.usage.output_tokens')" = "8000"
printf '%s' "$economics" | jq -e '.by_agent_workflow["workflow-cost-demo"] != null' >/dev/null
echo "cost spike demo passed: request_id=$request_id has versioned-price unit economics"
