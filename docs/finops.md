# FinOps

## Cost classification

| Component | Classification | Local source |
| --- | --- | --- |
| input/output/cached tokens | estimated | versioned `fixtures/prices.json` catalog |
| GPU-time component | simulated | local fixture duration × fixture GPU-hour rate |
| aggregate unit economics | estimated + simulated | persisted metadata-only usage events |

Money uses `Decimal`. Each catalog price has an effective timestamp, source, and version. If a
required price is unavailable, calculation records `PRICE_UNKNOWN`; it never silently substitutes
zero. The local results are not invoices or cloud-billing reconciliation.

## Available local views

`GET /api/v1/costs` returns cost events scoped to the caller’s tenant unless the local FinOps role
is used. `GET /api/v1/unit-economics?live_only=true` groups persisted live metadata by tenant,
model, and optional agent workflow and includes cost per request.

The local `finops-demo` bearer token is a non-secret fixture identity. It demonstrates scope
separation, not production authentication.

## Recommendations

`GET /api/v1/recommendations?live_only=true` computes deterministic suggestions from observed local
metadata: average TTFT/queue/tool duration, a queue-delay what-if, capacity state, and high-output
token advice. These suggestions never apply changes and must not be interpreted as GPU utilization,
autoscaling, or financial forecasts.
