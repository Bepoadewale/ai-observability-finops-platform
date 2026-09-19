from __future__ import annotations

import json
from pathlib import Path

from aiops.correlation.service import AnalyticsService
from aiops.cost.engine import CostEngine, PriceCatalog
from aiops.models.domain import Budget, PricingEntry, UsageEvent
from fastapi import Depends, FastAPI, Header, HTTPException

ROOT = Path(__file__).parents[3]
prices = [PricingEntry.model_validate(item) for item in json.loads((ROOT / "fixtures/prices.json").read_text())]
events = [UsageEvent.model_validate(item) for item in json.loads((ROOT / "fixtures/golden-events.json").read_text())]
service = AnalyticsService(CostEngine(PriceCatalog(prices)), events)
budgets: list[Budget] = []
app = FastAPI(title="AI Observability + FinOps Platform", version="0.1.0")


def principal(authorization: str = Header(...)) -> tuple[str, str]:
    # Demo auth only: maps opaque local tokens to scopes; no tenant header is trusted.
    tokens = {"Bearer tenant-search": ("tenant", "team-search"), "Bearer tenant-payments": ("tenant", "team-payments"), "Bearer finops-demo": ("finops", "*")}
    if authorization not in tokens: raise HTTPException(401, "invalid credentials")
    return tokens[authorization]


def scoped_tenant(identity: tuple[str, str], requested: str | None = None) -> str | None:
    role, tenant = identity
    if role == "tenant" and requested and requested != tenant: raise HTTPException(403, "tenant scope denied")
    return tenant if role == "tenant" else requested


@app.get("/healthz")
def healthz(): return {"status": "ok"}

@app.get("/api/v1/costs")
def costs(tenant_id: str | None = None, identity=Depends(principal)):
    return service.costs(scoped_tenant(identity, tenant_id))

@app.get("/api/v1/costs/tenants/{tenant_id}")
def tenant_cost(tenant_id: str, identity=Depends(principal)):
    return service.costs(scoped_tenant(identity, tenant_id))

@app.get("/api/v1/usage")
def usage(identity=Depends(principal)):
    tenant = scoped_tenant(identity)
    data = [item for item in service.usage if tenant is None or item.tenant_id == tenant]
    return {"events": [item.model_dump(mode="json") for item in data], "classification": "synthetic demo telemetry"}

@app.get("/api/v1/requests/{request_id}/analysis")
def request_analysis(request_id: str, identity=Depends(principal)):
    analysis = service.analysis(request_id)
    scoped_tenant(identity, next(e.tenant_id for e in service.usage if e.request_id == request_id))
    return analysis

@app.get("/api/v1/slo")
def slo(identity=Depends(principal)):  # auth keeps SLO signals from becoming an anonymous data source
    scoped_tenant(identity)
    return service.slo()

@app.get("/api/v1/efficiency")
def efficiency(identity=Depends(principal)):
    if identity[0] != "finops": raise HTTPException(403, "finops role required")
    return service.efficiency()

@app.get("/api/v1/budgets")
def list_budgets(identity=Depends(principal)):
    tenant = scoped_tenant(identity)
    return [b.model_dump(mode="json") for b in budgets if tenant is None or (b.scope_type == "tenant" and b.scope_id == tenant)]

@app.post("/api/v1/budgets")
def create_budget(budget: Budget, identity=Depends(principal)):
    if identity[0] != "finops": raise HTTPException(403, "finops role required")
    budgets.append(budget)
    return budget
