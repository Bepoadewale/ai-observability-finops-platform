output "cluster_name" {
  value       = module.eks.cluster_name
  description = "Future private EKS cluster name."
}

output "ecr_repository_url" {
  value       = aws_ecr_repository.analytics.repository_url
  description = "Immutable-image repository for the analytics API."
}

output "database_endpoint" {
  value       = module.data.database_endpoint
  description = "Private PostgreSQL endpoint. Do not expose it publicly."
  sensitive   = true
}

output "analytics_irsa_role_arn" {
  value       = module.workload_identity.role_arn
  description = "Narrow workload identity role; it is not an operator credential."
}

output "alb_controller_irsa_role_arn" {
  value       = module.alb_controller_identity.role_arn
  description = "Future AWS Load Balancer Controller role; not a browser or operator credential."
}
