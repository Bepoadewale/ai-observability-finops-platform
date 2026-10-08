variable "aws_region" {
  description = "AWS Region for the future pilot."
  type        = string
  default     = "us-east-1"
}

variable "expected_account_id" {
  description = "Account guardrail. A plan or apply fails in every other account."
  type        = string
}

variable "project" {
  description = "Project-scoped resource prefix and tag value."
  type        = string
  default     = "ai-observability-finops-platform"
}

variable "environment" {
  description = "Short-lived pilot environment name."
  type        = string
  default     = "pilot"
}

variable "vpc_cidr" {
  description = "Private address space reserved for the pilot VPC."
  type        = string
  default     = "10.82.0.0/16"
}

variable "availability_zones" {
  description = "At least two zones are needed for the private EKS control-plane design."
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "db_instance_class" {
  description = "Smallest intended RDS PostgreSQL instance class for a bounded pilot."
  type        = string
  default     = "db.t4g.micro"
}

variable "rds_deletion_protection" {
  description = "Keep true except during a reviewed Terraform destroy of the short-lived pilot."
  type        = bool
  default     = true
}

variable "monthly_budget_usd" {
  description = "Budget guardrail also used by the bootstrap root."
  type        = number
  default     = 10
}

variable "budget_alert_email" {
  description = "Email address for the future AWS Budget alarm. Never commit a real value."
  type        = string
  sensitive   = true
}
