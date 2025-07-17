output "cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = aws_eks_cluster.op_stack.endpoint
}

output "cluster_name" {
  description = "EKS cluster name"
  value       = aws_eks_cluster.op_stack.name
}

output "configure_kubectl" {
  description = "Configure kubectl command"
  value       = "aws eks --region us-west-2 update-kubeconfig --name ${aws_eks_cluster.op_stack.name}"
}

output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.op_stack_vpc.id
}
