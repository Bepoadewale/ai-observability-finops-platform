# Demo guide

## Primary request-correlation demo

`make demo-local` sends a completion request to the local workload and verifies:

1. the returned request ID and trace ID match analytics request analysis;
2. Prometheus has a generated `ai_requests_total` series; and
3. Tempo returns the generated trace.

The analysis contains metadata only: model, token counts, TTFT, TPOT, end-to-end latency, queue and
tool duration, estimated cost, and SLO state. Prompt and response content are not returned.

## Diagnostic scenarios

| Command | Input characteristic | Expected evidence |
| --- | --- | --- |
| `make demo-degradation` | high TTFT and queue delay | diagnosis calls out interactive TTFT and queueing |
| `make demo-tool-bottleneck` | tool duration dominates | diagnosis identifies tool latency, not model latency |
| `make demo-cost-spike` | 8,000 output-token fixture | workflow unit-economics entry exists |
| `make demo-saturation` | bounded high-queue burst | `SATURATED` capacity state and non-autonomous recommendation |
| `make demo-recovery` | analytics API restart | same live request remains analyzable after restart |
| `make demo-dashboard` | provisioned dashboard query | Grafana reports dashboard panels and Prometheus has data |

The scenarios are deterministic test inputs. They validate diagnostics but do not represent measured
production workload distributions or sizing advice.
