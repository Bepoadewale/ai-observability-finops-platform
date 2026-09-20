# Validation

Run `make test lint`; for end-to-end validation run `make bootstrap`, a telemetry generator, then query Prometheus and Tempo and capture only real dashboard screenshots. Record versions, services, commands/results, integration evidence, failure demos, and environment assumptions in `PROJECT_STATUS.md`. Never fabricate validation.

## Clean-Room Validation

Do not populate this section until executed. Record: date, commit SHA, OS/environment, Docker/kind/Kubernetes and key dependency versions where applicable; clean starting state; exact install/bootstrap/smoke/demo/failure/validation/cleanup commands; observed results; post-cleanup absence verification; and the second-bootstrap result. No prior local state or fabricated evidence is acceptable.
