variable "expected_account_id" { type = string }
variable "budget_alert_email" {
  type      = string
  sensitive = true
}
variable "monthly_budget_usd" {
  type    = number
  default = 10
}
variable "project" {
  type    = string
  default = "ai-observability-finops-platform"
}
