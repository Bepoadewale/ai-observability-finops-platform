# Contributing

Run `make lint`, `make test`, and `make verify` before proposing changes. For changes to the local
stack or telemetry flow, also run `make bootstrap-local`, `make smoke`, and the relevant demo target.
Preserve explicit units, timezone-aware UTC timestamps, `Decimal` money arithmetic, bounded metrics
labels, and data classification labels. Do not add prompts, completions, or secrets to telemetry.
