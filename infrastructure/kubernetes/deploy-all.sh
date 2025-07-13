#!/bin/bash
set -e

echo "🚀 Deploying Complete OP Stack to Kubernetes"
echo "============================================"

# Apply all manifests in order
kubectl apply -f namespace.yaml
echo "✅ Namespace created"

kubectl apply -f configmap.yaml
echo "✅ Configuration applied"

kubectl apply -f l1-ethereum.yaml
echo "✅ L1 Ethereum deployed"

kubectl apply -f l2-opstack.yaml
echo "✅ L2 OP Stack deployed"

echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=Ready pod -l app=l1-ethereum -n op-stack --timeout=300s
kubectl wait --for=condition=Ready pod -l app=l2-opstack -n op-stack --timeout=300s

echo "🎉 Deployment complete!"
echo ""
./k8s-demo.sh
