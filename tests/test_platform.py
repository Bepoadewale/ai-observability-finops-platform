from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from aiops.cost.engine import CostEngine, PriceCatalog
from aiops.main import app, prices
from aiops.models.domain import UsageEvent
from aiops.storage import UsageStore
from fastapi.testclient import TestClient


def event(**changes):
    payload = {"event_id":"x", "timestamp":datetime(2026, 9, 19, tzinfo=UTC), "tenant_id":"team-search", "team":"search", "cost_center":"cc", "request_id":"r", "trace_id":"t", "model":"llama-small", "deployment":"v1", "input_tokens":1_000_000, "output_tokens":1_000_000, "ttft_ms":100, "tpot_ms":10, "e2e_ms":1000}
    payload.update(changes)
    return UsageEvent(**payload)


def test_decimal_model_cost_and_price_version():
    costs = CostEngine(PriceCatalog(prices)).model_cost(event())
    assert CostEngine.total(costs) == Decimal("1.000000")


def test_request_analysis_is_correlated_and_privacy_safe():
    client = TestClient(app)
    response = client.get("/api/v1/requests/req-tool/analysis", headers={"Authorization":"Bearer tenant-payments"})
    assert response.status_code == 200
    assert "Tool execution dominates" in response.json()["diagnostic_hints"][0]
    assert "prompt" not in str(response.json()).lower()


def test_tenant_cannot_read_another_tenant_cost():
    client = TestClient(app)
    response = client.get("/api/v1/costs/tenants/team-payments", headers={"Authorization":"Bearer tenant-search"})
    assert response.status_code == 403


def test_finops_efficiency_recommends_no_unsafe_capacity_cut():
    client = TestClient(app)
    response = client.get("/api/v1/efficiency", headers={"Authorization":"Bearer finops-demo"})
    assert response.status_code == 200
    assert response.json()["state"] == "SATURATED"


def test_only_telemetry_producer_can_ingest_metadata_event():
    client = TestClient(app)
    payload = event(event_id=f"live-{uuid4()}", request_id=f"request-{uuid4()}").model_dump(mode="json")
    denied = client.post("/api/v1/usage", json=payload, headers={"Authorization": "Bearer tenant-search"})
    accepted = client.post(
        "/api/v1/usage", json=payload, headers={"Authorization": "Bearer telemetry-producer"}
    )
    duplicate = client.post(
        "/api/v1/usage", json=payload, headers={"Authorization": "Bearer telemetry-producer"}
    )
    assert denied.status_code == 403
    assert accepted.json()["accepted"] is True
    assert duplicate.json()["accepted"] is False


def test_usage_store_survives_service_reconstruction(tmp_path):
    stored = event(event_id="durable-event", request_id="durable-request")
    store = UsageStore(tmp_path / "usage.db")
    assert store.insert(stored) is True
    rebuilt = UsageStore(tmp_path / "usage.db")
    assert rebuilt.list_events() == [stored]
