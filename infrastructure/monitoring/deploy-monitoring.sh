#!/bin/bash
echo "🚀 Deploying Monitoring Stack"
echo "============================="

# Apply monitoring components
kubectl apply -f prometheus-config.yaml
kubectl apply -f prometheus-deployment.yaml
kubectl apply -f grafana-deployment.yaml

echo "⏳ Waiting for deployments..."
kubectl wait --for=condition=Ready pod -l app=prometheus -n op-stack --timeout=120s
kubectl wait --for=condition=Ready pod -l app=grafana -n op-stack --timeout=120s

echo "✅ Monitoring stack deployed!"
echo ""
echo "📊 Access URLs:"
echo "   Prometheus: http://localhost:30003"
echo "   Grafana: http://localhost:30004 (admin/admin123)"
