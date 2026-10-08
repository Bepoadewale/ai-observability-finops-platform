#!/usr/bin/env bash
set -euo pipefail

# Read-only future cost-evidence query. AWS often publishes settled values 24–48 hours later.
: "${AWS_PROFILE:?Set AWS_PROFILE to a read-only or operator profile.}"
: "${START_DATE:?Set START_DATE as YYYY-MM-DD.}"
: "${END_DATE:?Set END_DATE as YYYY-MM-DD.}"

aws ce get-cost-and-usage \
  --profile "$AWS_PROFILE" \
  --time-period "Start=$START_DATE,End=$END_DATE" \
  --granularity DAILY \
  --metrics UnblendedCost UsageQuantity \
  --group-by Type=TAG,Key=Project \
  --output json
