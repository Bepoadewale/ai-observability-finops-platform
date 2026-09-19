from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class CostType(StrEnum):
    ACTUAL = "actual"
    ESTIMATED = "estimated"
    ALLOCATED = "allocated"
    FORECAST = "forecast"
    SIMULATED = "simulated"


class PricingEntry(BaseModel):
    sku: str
    unit: Literal["million_tokens", "gpu_hour", "cpu_core_hour", "gb_hour"]
    price: Decimal = Field(ge=0)
    currency: str = "USD"
    effective_from: datetime
    source: str
    version: str

    @field_validator("effective_from")
    @classmethod
    def utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("effective_from must be timezone-aware")
        return value.astimezone(UTC)


class UsageEvent(BaseModel):
    event_id: str
    timestamp: datetime
    tenant_id: str
    team: str
    cost_center: str
    request_id: str
    trace_id: str
    model: str
    deployment: str
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)
    cached_tokens: int = Field(default=0, ge=0)
    ttft_ms: int = Field(ge=0)
    tpot_ms: int = Field(ge=0)
    e2e_ms: int = Field(ge=0)
    queue_ms: int = Field(default=0, ge=0)
    tool_ms: int = Field(default=0, ge=0)
    success: bool = True
    agent_run_id: str | None = None

    @field_validator("timestamp")
    @classmethod
    def timestamp_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("timestamp must be timezone-aware")
        return value.astimezone(UTC)


class GpuSample(BaseModel):
    timestamp: datetime
    model: str
    tenant_id: str | None = None
    gpu_count: int = Field(ge=0)
    utilization_percent: Decimal = Field(ge=0, le=100)
    memory_percent: Decimal = Field(ge=0, le=100)
    power_watts: Decimal = Field(ge=0)
    simulated: bool = True


class Budget(BaseModel):
    id: str
    scope_type: Literal["tenant", "team", "model"]
    scope_id: str
    monthly_amount: Decimal = Field(gt=0)
    currency: str = "USD"


class CostEvent(BaseModel):
    event_id: str
    timestamp: datetime
    tenant_id: str
    request_id: str | None = None
    trace_id: str | None = None
    model: str | None = None
    resource_type: str
    quantity: Decimal
    unit: str
    unit_price: Decimal | None = None
    currency: str = "USD"
    cost: Decimal | None = None
    cost_type: CostType
    pricing_source: str
    pricing_version: str
