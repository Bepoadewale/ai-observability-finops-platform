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
