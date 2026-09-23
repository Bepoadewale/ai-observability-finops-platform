#!/usr/bin/env bash
set -euo pipefail

# Use a bounded burst so this scenario remains dominant even after the normal,
# latency, and cost demonstrations have populated the durable local store.
for _ in $(seq 1 10); do
  curl -fsS http://127.0.0.1:8081/v1/chat/completions \
    -H 'content-type: application/json' \
    -d '{"tenant_id":"team-search","model":"llama-small","prompt":"saturation sample","scenario":"saturation"}' >/dev/null
done

for _ in $(seq 1 20); do
  efficiency=$(curl -fsS 'http://127.0.0.1:8080/api/v1/efficiency?live_only=true' -H 'Authorization: Bearer finops-demo')
  if test "$(printf '%s' "$efficiency" | jq -r '.state')" = "SATURATED"; then
    break
  fi
  sleep 1
done
test "$(printf '%s' "$efficiency" | jq -r '.state')" = "SATURATED"
printf '%s' "$efficiency" | jq -e '.recommendations[] | contains("evaluate capacity")' >/dev/null
echo "saturation demo passed: observed queueing produces a bounded capacity recommendation"
