variable "name" { type = string }
variable "oidc_provider_arn" { type = string }
variable "oidc_issuer_host" { type = string }
variable "namespace" { type = string }
variable "service_account" { type = string }
variable "evidence_bucket_arn" { type = string }
variable "runtime_secret_arn" { type = string }

data "aws_iam_policy_document" "assume" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]
    principals {
      type        = "Federated"
      identifiers = [var.oidc_provider_arn]
    }
    condition {
      test     = "StringEquals"
      variable = "${var.oidc_issuer_host}:sub"
      values   = ["system:serviceaccount:${var.namespace}:${var.service_account}"]
    }
    condition {
      test     = "StringEquals"
      variable = "${var.oidc_issuer_host}:aud"
      values   = ["sts.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "analytics" {
  name               = "${var.name}-analytics-api"
  assume_role_policy = data.aws_iam_policy_document.assume.json
}

data "aws_iam_policy_document" "analytics" {
  statement {
    sid       = "ReadApprovedPriceAndEvidenceObjects"
    effect    = "Allow"
    actions   = ["s3:GetObject", "s3:PutObject"]
    resources = ["${var.evidence_bucket_arn}/*"]
  }
  statement {
    sid       = "ReadOnlyRuntimeSecret"
    effect    = "Allow"
    actions   = ["secretsmanager:GetSecretValue"]
    resources = [var.runtime_secret_arn]
  }
}

resource "aws_iam_role_policy" "analytics" {
  name   = "${var.name}-analytics-runtime"
  role   = aws_iam_role.analytics.id
  policy = data.aws_iam_policy_document.analytics.json
}

output "role_arn" { value = aws_iam_role.analytics.arn }
