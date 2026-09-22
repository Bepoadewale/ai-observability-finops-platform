#!/usr/bin/env bash
set -euo pipefail

wait_for() {
  local name="$1"
  local url="$2"
  for _ in $(seq 1 60); do
    if curl -fsS "$url" >/dev/null 2>&1; then
      echo "$name ready"
      return 0
    fi
    sleep 1
  done
  echo "$name did not become ready: $url" >&2
  exit 1
}

wait_for analytics-api http://127.0.0.1:8080/healthz
wait_for demo-ai http://127.0.0.1:8081/healthz
wait_for prometheus http://127.0.0.1:9090/-/ready
wait_for tempo http://127.0.0.1:3200/ready
wait_for grafana http://127.0.0.1:3000/api/health
