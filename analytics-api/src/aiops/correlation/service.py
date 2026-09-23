from __future__ import annotations

from decimal import Decimal

from aiops.cost.engine import CostEngine, PriceUnknown
from aiops.models.domain import UsageEvent
from aiops.storage import UsageStore


class AnalyticsService:
    def __init__(self, engine: CostEngine, fixture_usage: list[UsageEvent], store: UsageStore | None = None):
        self.engine, self.store = engine, store
        self.fixture_usage = fixture_usage
        self.usage = [*fixture_usage, *(store.list_events() if store else [])]
        self._seen = {item.event_id for item in self.usage}

    def ingest(self, event: UsageEvent) -> bool:
        if event.event_id in self._seen:
            return False
        if self.store and not self.store.insert(event):
            self._seen.add(event.event_id)
            return False
        self._seen.add(event.event_id)
        self.usage.append(event)
        return True

    def live_usage(self) -> list[UsageEvent]:
        fixture_ids = {event.event_id for event in self.fixture_usage}
        return [event for event in self.usage if event.event_id not in fixture_ids]

    def costs(self, tenant: str | None = None) -> dict:
        items = [event for event in self.usage if tenant is None or event.tenant_id == tenant]
        costs = []
        unknown = []
        for item in items:
            try:
                costs.extend(self.engine.model_cost(item))
                costs.append(self.engine.gpu_cost(item, Decimal(item.e2e_ms) / Decimal(1000)))
            except PriceUnknown as exc:
                unknown.append(str(exc))
        return {"cost_type": "estimated_and_simulated", "currency": "USD", "total": str(self.engine.total(costs)),
                "events": [c.model_dump(mode="json") for c in costs], "price_unknown": unknown}

    def analysis(self, request_id: str) -> dict:
        event = next((item for item in self.usage if item.request_id == request_id), None)
        if not event:
            raise KeyError(request_id)
        costs = self.costs(event.tenant_id)["events"]
        request_cost = sum((Decimal(c["cost"]) for c in costs if c["request_id"] == request_id), Decimal(0))
        hints = []
        if event.queue_ms > event.e2e_ms * .25: hints.append("Queueing is a material part of end-to-end latency.")
        if event.tool_ms > event.e2e_ms * .5: hints.append("Tool execution dominates this request; model latency is not the primary bottleneck.")
        if event.ttft_ms > 1000: hints.append("TTFT exceeds the interactive example objective; inspect queueing and model prefill.")
        telemetry_classification = "live metadata-only telemetry" if event in self.live_usage() else "synthetic fixture telemetry"
        return {"request_id": request_id, "trace_id": event.trace_id, "classification": {"cost": "estimated/simulated", "telemetry": telemetry_classification},
                "performance": {"e2e_ms": event.e2e_ms, "ttft_ms": event.ttft_ms, "tpot_ms": event.tpot_ms, "queue_ms": event.queue_ms, "tool_ms": event.tool_ms},
                "usage": {"model": event.model, "deployment": event.deployment, "input_tokens": event.input_tokens, "output_tokens": event.output_tokens, "success": event.success},
                "cost": {"estimated_total": str(request_cost), "currency": "USD"},
                "slo": self.slo(events=self.live_usage()), "diagnostic_hints": hints}

    def slo(self, threshold_ms: int = 1000, events: list[UsageEvent] | None = None) -> dict:
        items = self.usage if events is None else events
        if not items: return {"name": "interactive-chat-ttft", "compliance": "1.0000", "remaining_error_budget": "1.0000", "bad_events": 0, "events": 0}
        good = sum(event.success and event.ttft_ms <= threshold_ms for event in items)
        compliance = Decimal(good) / Decimal(len(items))
        target = Decimal("0.95")
        return {"name": "interactive-chat-ttft", "target": str(target), "compliance": str(compliance.quantize(Decimal("0.0001"))),
                "remaining_error_budget": str(max(Decimal(0), (compliance - target) / (Decimal(1) - target)).quantize(Decimal("0.0001"))),
                "bad_events": len(items) - good, "events": len(items)}

    def efficiency(self) -> dict:
        if not self.usage: return {"state": "HEALTHY", "recommendations": []}
        avg_queue = sum(e.queue_ms for e in self.usage) / len(self.usage)
        avg_ttft = sum(e.ttft_ms for e in self.usage) / len(self.usage)
        state = "SATURATED" if avg_queue > 400 else "HEALTHY"
        return {"state": state, "evidence": {"avg_queue_ms": avg_queue, "avg_ttft_ms": avg_ttft}, "recommendations": (["High queueing and TTFT: evaluate capacity or batching; do not reduce capacity."] if state == "SATURATED" else ["No capacity reduction recommendation without utilization and SLO headroom."])}
