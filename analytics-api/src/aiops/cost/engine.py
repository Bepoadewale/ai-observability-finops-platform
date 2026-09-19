from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal

from aiops.models.domain import CostEvent, CostType, PricingEntry, UsageEvent

MILLION = Decimal(1000000)
CENTS = Decimal("0.000001")


class PriceUnknown(Exception):
    pass


class PriceCatalog:
    def __init__(self, entries: list[PricingEntry]):
        self.entries = entries

    def get(self, sku: str, at: datetime) -> PricingEntry:
        candidates = [p for p in self.entries if p.sku == sku and p.effective_from <= at]
        if not candidates:
            raise PriceUnknown(f"PRICE_UNKNOWN:{sku}")
        return max(candidates, key=lambda price: price.effective_from)


class CostEngine:
    def __init__(self, catalog: PriceCatalog):
        self.catalog = catalog

    def model_cost(self, event: UsageEvent) -> list[CostEvent]:
        result: list[CostEvent] = []
        for kind, quantity in (("input", event.input_tokens), ("output", event.output_tokens), ("cached", event.cached_tokens)):
            if not quantity:
                continue
            price = self.catalog.get(f"model:{event.model}:{kind}", event.timestamp)
            cost = (Decimal(quantity) / MILLION * price.price).quantize(CENTS, rounding=ROUND_HALF_UP)
            result.append(CostEvent(event_id=f"cost:{event.event_id}:{kind}", timestamp=event.timestamp,
                tenant_id=event.tenant_id, request_id=event.request_id, trace_id=event.trace_id,
                model=event.model, resource_type=f"model_{kind}_tokens", quantity=Decimal(quantity),
                unit="tokens", unit_price=price.price, cost=cost, cost_type=CostType.ESTIMATED,
                pricing_source=price.source, pricing_version=price.version))
        return result

    def gpu_cost(self, event: UsageEvent, gpu_seconds: Decimal, simulated: bool = True) -> CostEvent:
        price = self.catalog.get(f"compute:{event.model}:gpu_hour", event.timestamp)
        cost = (gpu_seconds / Decimal(3600) * price.price).quantize(CENTS, rounding=ROUND_HALF_UP)
        return CostEvent(event_id=f"cost:{event.event_id}:gpu", timestamp=event.timestamp, tenant_id=event.tenant_id,
            request_id=event.request_id, trace_id=event.trace_id, model=event.model, resource_type="gpu",
            quantity=gpu_seconds, unit="gpu_seconds", unit_price=price.price, cost=cost,
            cost_type=CostType.SIMULATED if simulated else CostType.ESTIMATED,
            pricing_source=price.source, pricing_version=price.version)

    @staticmethod
    def total(events: list[CostEvent]) -> Decimal:
        return sum((event.cost or Decimal(0) for event in events), Decimal(0))

    @staticmethod
    def allocate_shared(total: Decimal, usage: list[UsageEvent]) -> dict[str, Decimal]:
        weights: dict[str, int] = defaultdict(int)
        for event in usage:
            weights[event.tenant_id] += event.input_tokens + event.output_tokens
        denominator = sum(weights.values())
        if not denominator:
            return {}
        return {tenant: (total * Decimal(weight) / Decimal(denominator)).quantize(CENTS, rounding=ROUND_HALF_UP)
                for tenant, weight in weights.items()}
