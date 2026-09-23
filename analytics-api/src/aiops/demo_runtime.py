"""A deterministic AI-workload fixture that emits real local telemetry.

It deliberately does not persist prompts or responses in metrics, traces, or the
analytics API. Its job is to make the observability control loop executable,
not to represent a production model benchmark.
"""

from __future__ import annotations

import os
from datetime import UTC, datetime
from time import perf_counter
from uuid import uuid4

import httpx
from fastapi import FastAPI, HTTPException
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_client import Counter, Histogram, make_asgi_app
from pydantic import BaseModel, Field

REQUESTS = Counter("ai_requests_total", "Demo AI workload requests", ["tenant", "outcome"])
TOKENS = Counter("ai_request_tokens_total", "Demo AI workload tokens", ["model", "type"])
LATENCY = Histogram("ai_request_duration_seconds", "Demo AI request latency", ["model"])
TTFT = Histogram("ai_request_ttft_seconds", "Demo AI time to first token", ["model"])
QUEUE = Histogram("ai_request_queue_seconds", "Demo AI queue duration", ["scenario"])
TOOL = Histogram("ai_tool_duration_seconds", "Demo AI tool duration", ["scenario"])
INGEST_FAILURES = Counter("ai_telemetry_ingest_failures_total", "Analytics ingestion failures")

app = FastAPI(title="AI telemetry producer", version="0.1.0")
app.mount("/metrics", make_asgi_app())


class CompletionRequest(BaseModel):
    tenant_id: str = Field(pattern="^team-(search|payments)$")
    model: str = "llama-small"
    prompt: str = Field(min_length=1, max_length=512)
    scenario: str = Field(default="normal", pattern="^(normal|latency|tool_bottleneck|cost_spike|saturation)$")
    agent_run_id: str | None = Field(default=None, max_length=128)


SCENARIOS = {
    "normal": {"ttft_ms": 120, "queue_ms": 20, "tool_ms": 15, "output_tokens": 24, "success": True},
    "latency": {"ttft_ms": 1_350, "queue_ms": 620, "tool_ms": 20, "output_tokens": 24, "success": True},
    "tool_bottleneck": {"ttft_ms": 180, "queue_ms": 40, "tool_ms": 1_100, "output_tokens": 24, "success": True},
    "cost_spike": {"ttft_ms": 180, "queue_ms": 40, "tool_ms": 15, "output_tokens": 8_000, "success": True},
    "saturation": {"ttft_ms": 1_600, "queue_ms": 900, "tool_ms": 30, "output_tokens": 24, "success": True},
}


def configure_tracing() -> None:
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if not endpoint:
        return
    provider = TracerProvider(resource=Resource.create({"service.name": "ai-telemetry-producer"}))
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=f"{endpoint}/v1/traces")))
    trace.set_tracer_provider(provider)
    FastAPIInstrumentor.instrument_app(app, tracer_provider=provider, excluded_urls="healthz,metrics")


@app.on_event("startup")
def startup() -> None:
    configure_tracing()


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok", "workload": "deterministic-ai-telemetry-fixture"}


@app.post("/v1/chat/completions")
async def complete(request: CompletionRequest) -> dict:
    profile = SCENARIOS.get(request.scenario)
    if profile is None:
        raise HTTPException(400, "unsupported scenario")
    started = perf_counter()
    request_id = str(uuid4())
    input_tokens = len(request.prompt.split())
    with trace.get_tracer("ai-telemetry-producer").start_as_current_span("gen_ai.inference") as span:
        span.set_attribute("ai.request_id", request_id)
        span.set_attribute("ai.tenant", request.tenant_id)
        span.set_attribute("gen_ai.request.model", request.model)
        span.set_attribute("gen_ai.usage.input_tokens", input_tokens)
        span.set_attribute("gen_ai.usage.output_tokens", profile["output_tokens"])
        span.set_attribute("ai.scenario", request.scenario)
        context = span.get_span_context()
        trace_id = f"{context.trace_id:032x}"
        e2e_ms = max(profile["ttft_ms"] + profile["queue_ms"] + profile["tool_ms"], int((perf_counter() - started) * 1000))
        event = {
            "event_id": f"usage-{request_id}",
            "timestamp": datetime.now(UTC).isoformat(),
            "tenant_id": request.tenant_id,
            "team": request.tenant_id.removeprefix("team-"),
            "cost_center": "local-demo",
            "request_id": request_id,
            "trace_id": trace_id,
            "model": request.model,
            "deployment": "local-fixture-v1",
            "input_tokens": input_tokens,
            "output_tokens": profile["output_tokens"],
            "cached_tokens": 0,
            "ttft_ms": profile["ttft_ms"],
            "tpot_ms": 12,
            "e2e_ms": e2e_ms,
            "queue_ms": profile["queue_ms"],
            "tool_ms": profile["tool_ms"],
            "success": profile["success"],
            "agent_run_id": request.agent_run_id,
        }
        try:
            async with httpx.AsyncClient(timeout=3) as client:
                response = await client.post(
                    os.getenv("ANALYTICS_INGEST_URL", "http://analytics-api:8080/api/v1/usage"),
                    headers={"Authorization": "Bearer telemetry-producer"},
                    json=event,
                )
                response.raise_for_status()
        except httpx.HTTPError:
            INGEST_FAILURES.inc()
            span.set_attribute("ai.telemetry.ingested", False)
        else:
            span.set_attribute("ai.telemetry.ingested", True)

    REQUESTS.labels(request.tenant_id, "success").inc()
    TOKENS.labels(request.model, "input").inc(input_tokens)
    TOKENS.labels(request.model, "output").inc(profile["output_tokens"])
    LATENCY.labels(request.model).observe(e2e_ms / 1000)
    TTFT.labels(request.model).observe(profile["ttft_ms"] / 1000)
    QUEUE.labels(request.scenario).observe(profile["queue_ms"] / 1000)
    TOOL.labels(request.scenario).observe(profile["tool_ms"] / 1000)
    return {
        "id": request_id,
        "model": request.model,
        "response": "deterministic local AI workload response",
        "telemetry": {"request_id": request_id, "trace_id": trace_id, "raw_prompt_recorded": False},
    }
