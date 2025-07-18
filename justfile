# Infrastructure automation commands

# Validate all infrastructure
validate:
    cd infrastructure/terraform/aws-eks && terraform validate
    kubectl --dry-run=client apply -f infrastructure/kubernetes/

# Deploy to development
deploy-dev:
    cd infrastructure/terraform/aws-eks && terraform plan

# Deploy to production
deploy-prod:
    cd infrastructure/terraform/aws-eks && terraform apply

# Test monitoring
test-monitoring:
    curl -s http://localhost:9090/api/v1/query?query=up
    curl -s http://localhost:3000

# Lint documentation
lint-docs:
    markdownlint-cli2 "**/*.md"
