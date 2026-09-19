# High TTFT runbook

Check queue depth, running/waiting inference requests, model deployment markers, KV-cache pressure and tool spans. If GPU utilization is low, investigate routing/prefill/network before adding capacity. If utilization and queue are both high, evaluate capacity and batching with SLO headroom.
