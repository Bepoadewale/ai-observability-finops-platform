# Failure modes

When telemetry backends are unavailable, serving must continue and data quality must report gaps. Pricing lookup failure returns `PRICE_UNKNOWN`; duplicate usage is rejected by event ID; partial traces do not invent missing cost. Monitor collector drops, exporter failures, scrape failures and cost-processing lag.
