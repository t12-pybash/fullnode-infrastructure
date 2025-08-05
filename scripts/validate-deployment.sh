#!/bin/bash
set -e

echo "OP Stack Infrastructure Validation"
echo "===================================="

# Check AWS EKS cluster
echo "Checking EKS cluster..."
aws eks describe-cluster --name op-stack-cluster --region us-west-2 --query 'cluster.status'

# Check kubectl connectivity
echo "Checking kubectl connectivity..."
kubectl cluster-info

# Check namespace
echo "Checking namespace..."
kubectl get namespace op-stack

# Check all pods
echo "Checking pod status..."
kubectl get pods -n op-stack

# Check services
echo "Checking services..."
kubectl get services -n op-stack

# Check nodes
echo "Checking nodes..."
kubectl get nodes

# Test blockchain connectivity
echo "Testing blockchain connectivity..."
kubectl port-forward -n op-stack svc/l1-ethereum-simple-service 8545:8545 &
PF_PID=$!
sleep 5

if curl -s -X POST -H "Content-Type: application/json" \
   --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' \
   http://localhost:8545 | grep -q result; then
  echo "L1 Ethereum node is responding"
else
  echo "L1 Ethereum node not responding"
fi

kill $PF_PID 2>/dev/null || true

echo ""
echo "Infrastructure validation complete!"