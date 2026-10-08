# Cloud Operations

The cloud pilot will be off by default because it creates billable AWS resources.
Terraform will be the only create/destroy mechanism. Before any apply, an operator
must review the account, region, tags, budget, and plan.

The pilot will record: a normal request, a latency/cost/failure scenario, metrics,
traces, dashboard evidence, alert evidence, a bounded load sample, an AWS cost query,
and Terraform teardown checks. Cost Explorer values remain estimates until AWS billing
settles, often 24–48 hours later.
