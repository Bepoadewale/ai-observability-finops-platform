provider "aws" {
  region = var.aws_region

  default_tags {
    tags = local.tags
  }
}

data "aws_caller_identity" "current" {}

locals {
  name = "${var.project}-${var.environment}"
  tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "terraform"
    Purpose     = "finops-cloud-pilot"
  }
}

check "expected_account" {
  assert {
    condition     = data.aws_caller_identity.current.account_id == var.expected_account_id
    error_message = "The AWS account does not match expected_account_id. Stop before changing resources."
  }
}

module "vpc" {
  source             = "../modules/vpc"
  name               = local.name
  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
  project            = var.project
}

module "eks" {
  source             = "../modules/eks"
  name               = local.name
  private_subnet_ids = module.vpc.private_subnet_ids
  kubernetes_version = "1.31"
}

resource "aws_ecr_repository" "analytics" {
  name                 = "${local.name}-analytics-api"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_secretsmanager_secret" "runtime" {
  name                    = "${local.name}/runtime"
  recovery_window_in_days = 7
}

module "data" {
  source               = "../modules/data"
  name                 = local.name
  vpc_id               = module.vpc.vpc_id
  private_subnet_ids   = module.vpc.private_subnet_ids
  private_subnet_cidrs = module.vpc.private_subnet_cidrs
  db_instance_class    = var.db_instance_class
}

module "workload_identity" {
  source              = "../modules/iam"
  name                = local.name
  oidc_provider_arn   = module.eks.oidc_provider_arn
  oidc_issuer_host    = module.eks.oidc_issuer_host
  namespace           = "ai-observability"
  service_account     = "analytics-api"
  evidence_bucket_arn = module.data.evidence_bucket_arn
  runtime_secret_arn  = aws_secretsmanager_secret.runtime.arn
}

module "alb_controller_identity" {
  source            = "../modules/alb-controller"
  name              = local.name
  oidc_provider_arn = module.eks.oidc_provider_arn
  oidc_issuer_host  = module.eks.oidc_issuer_host
}
