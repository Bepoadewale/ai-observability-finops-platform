# Cloud Delivery Design

This page describes how a future AWS pilot will deliver the analytics service. It is a
checked-in plan, not proof that the service has run in AWS.

## The intended path

```text
reviewed source change
  → CI builds and scans an immutable ECR image
  → reviewed Git change updates the image digest
  → Argo CD reads this repository
  → private EKS applies the workload contract
  → health checks decide whether the Pod is ready
```

The API process will not run `kubectl`, Helm, or Terraform. Terraform creates the AWS
foundation. Git holds the desired Kubernetes state. Argo CD is the component that
reconciles that state into EKS.

## What is deliberately narrow

The initial ingress contract creates an **internal** Application Load Balancer route for
only `/api` and `/docs`. It does not route Prometheus, Tempo, Grafana administration,
PostgreSQL, Kubernetes, or Secrets Manager. It stays internal because the current API
uses local fixture tokens. A public route cannot be safe until the platform adds trusted
OIDC login, exact browser redirect URLs, exact CORS origins, and tests for those controls.

## Image and secret rules

The future ECR repository rejects mutable tags and scans images on push. The deployed
manifest must use an image digest, not a floating tag. External Secrets will supply the
database connection value at runtime. The manifest contains only a secret name and key,
not a value.

## Runtime bootstrap boundary

Before Argo CD can apply the application, an operator must install the AWS Load Balancer
Controller with its dedicated IRSA role, install External Secrets with its own narrowed
role, publish the immutable image, migrate the application to PostgreSQL, and replace the
explicit deployment placeholders. Those steps need readiness checks and cloud evidence;
they are not performed by this PR.
