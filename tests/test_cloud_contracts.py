from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_cloud_workload_has_required_pod_security_controls():
    manifest = (ROOT / "infrastructure/kubernetes/cloud/analytics-api.yaml").read_text()
    for required in (
        "runAsNonRoot: true",
        "allowPrivilegeEscalation: false",
        'drop: ["ALL"]',
        "readOnlyRootFilesystem: true",
        "type: RuntimeDefault",
        "readinessProbe:",
        "livenessProbe:",
        "kind: PodDisruptionBudget",
    ):
        assert required in manifest


def test_cloud_network_contract_starts_with_default_deny():
    manifest = (ROOT / "infrastructure/kubernetes/cloud/network-policies.yaml").read_text()
    assert "name: default-deny" in manifest
    assert 'policyTypes: ["Ingress", "Egress"]' in manifest


def test_pilot_contract_keeps_runtime_private_and_uses_irsa():
    pilot = (ROOT / "infrastructure/terraform/pilot/main.tf").read_text()
    eks = (ROOT / "infrastructure/terraform/modules/eks/main.tf").read_text()
    iam = (ROOT / "infrastructure/terraform/modules/iam/main.tf").read_text()
    assert "endpoint_public_access  = false" in eks
    assert "aws_iam_openid_connect_provider" in eks
    assert "sts:AssumeRoleWithWebIdentity" in iam
    assert "aws_secretsmanager_secret" in pilot


def test_data_contract_encrypts_and_does_not_publish_database():
    data = (ROOT / "infrastructure/terraform/modules/data/main.tf").read_text()
    assert "publicly_accessible         = false" in data
    assert "storage_encrypted           = true" in data
    assert "aws_s3_bucket_server_side_encryption_configuration" in data


def test_delivery_contract_uses_gitops_and_narrow_internal_ingress():
    ingress = (ROOT / "infrastructure/kubernetes/cloud/ingress.yaml").read_text()
    app = (ROOT / "infrastructure/argocd/ai-observability-finops.yaml").read_text()
    controller = (ROOT / "infrastructure/terraform/modules/alb-controller/main.tf").read_text()
    assert "alb.ingress.kubernetes.io/scheme: internal" in ingress
    assert "path: /api" in ingress
    assert "path: /docs" in ingress
    assert "prometheus" not in ingress.lower()
    assert "repoURL: https://github.com/Bepoadewale/ai-observability-finops-platform.git" in app
    assert "aws-load-balancer-controller" in controller


def test_cloud_delivery_never_commits_secret_values_or_mutable_image_tags():
    secret = (ROOT / "infrastructure/kubernetes/cloud/external-secret.yaml").read_text()
    deployment = (ROOT / "infrastructure/kubernetes/cloud/analytics-api.yaml").read_text()
    assert "database-url" in secret
    assert "postgres://" not in secret
    assert "REPLACED_BY_IMMUTABLE_ECR_DIGEST_AT_DEPLOY_TIME" in deployment


def test_observability_contract_has_sanitization_alerts_and_bounded_load():
    manifest = (ROOT / "infrastructure/kubernetes/cloud/observability.yaml").read_text()
    load = (ROOT / "infrastructure/load/cloud-bounded-load.js").read_text()
    assert "gen_ai.prompt" in manifest
    assert "gen_ai.response.content" in manifest
    assert "AIPlatformHighTTFT" in manifest
    assert "AIPlatformTelemetryTargetMissing" in manifest
    assert "vus: 2" in load
    assert "duration: '2m'" in load


def test_reliability_and_cost_scripts_are_bounded_and_read_only_by_design():
    ha = (ROOT / "scripts/cloud-verify-ha.sh").read_text()
    cost = (ROOT / "scripts/cloud-cost-evidence.sh").read_text()
    assert "--timeout=180s" in ha
    assert "get-cost-and-usage" in cost
    assert "aws ce" in cost
