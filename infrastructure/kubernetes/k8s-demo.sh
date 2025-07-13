#!/bin/bash
echo "🚀 OP Stack Kubernetes Deployment Demo"
echo "======================================"
echo
echo "📊 Cluster Status:"
kubectl get nodes
echo
echo "📦 OP Stack Namespace:"
kubectl get namespace op-stack
echo
echo "🔧 Pod Status:"
kubectl get pods -n op-stack -o wide
echo
echo "🌐 Services:"
kubectl get services -n op-stack
echo
echo "📈 Blockchain Status:"
echo -n "L1 Ethereum (port 8570): "
curl -s -X POST -H "Content-Type: application/json" \
  --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' \
  http://localhost:8570 | jq -r '.result' 2>/dev/null | xargs printf "Block %d\n" $(($(cat))) 2>/dev/null || echo "Starting..."

echo -n "L2 OP Stack (port 9570): "
curl -s -X POST -H "Content-Type: application/json" \
  --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' \
  http://localhost:9570 | jq -r '.result' 2>/dev/null | xargs printf "Block %d\n" $(($(cat))) 2>/dev/null || echo "Starting..."
echo
echo "✅ OP Stack running in Kubernetes!"
