## Objective

## Changes

## Validation

## Demonstrated Behavior

## Failure Cases Tested

## Remaining Gaps

## Status Changes

## Completion Gate Evidence

## Explicitly Unexecuted / Simulated Adapters

## Cloud-pilot evidence (required before a cloud-pilot PR is review-ready)

- [ ] Expected AWS account, region, tags, and budget were reviewed.
- [ ] Terraform plan output is linked or summarized; no unreviewed manual AWS change was used.
- [ ] Apply, smoke, security/failure drill, observability, and cost evidence are recorded when AWS ran.
- [ ] Destroy was account-confirmed and post-destroy absence was checked when the pilot was torn down.
- [ ] Claims are labeled as local execution, static validation, simulation, planned pilot, or executed cloud evidence.

## Clean-room completion gate (required before a final feature PR is review-ready)

- [ ] Clean project state established and verified.
- [ ] Bootstrap and smoke checks passed.
- [ ] Primary demo and required failure/security demo passed.
- [ ] Full required validation passed.
- [ ] Project-scoped cleanup passed; no project runtime resources remained unexpectedly.
- [ ] Second clean bootstrap passed.
- [ ] `docs/VALIDATION.md`, README commands, and `PROJECT_STATUS.md` were updated with real evidence.
