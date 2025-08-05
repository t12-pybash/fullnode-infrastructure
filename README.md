# Fullnode Infrastructure Engineering deployment

> Infrastructure automation and operational excellence for the Optimism ecosystem

## Overview
production-ready infrastructure environment for OP Stack deployment, monitoring, and operations.

## Quick Start
```bash
git clone https://github.com/t12-pybash/fullnode-infrastructure
cd op-stack-x-prep
./scripts/setup.sh

## Kubernetes Deployment

### Infrastructure Components
- **Namespace**: Isolated op-stack environment
- **StatefulSets**: Persistent blockchain nodes with storage
- **Services**: NodePort services for external access
- **ConfigMaps**: Environment configuration management
- **Resource Management**: CPU/memory limits and requests

### Live Demo
```bash
cd infrastructure/kubernetes
./k8s-demo.sh
Architecture
┌─────────────────┐    ┌─────────────────┐
│   L1 Ethereum   │    │   L2 OP Stack   │
│   StatefulSet   │    │   StatefulSet   │
│   Port: 8570    │    │   Port: 9570    │
└─────────────────┘    └─────────────────┘
        │                        │
        ▼                        ▼
   NodePort Svc            NodePort Svc
   10.96.226.52           10.96.79.1
Key Features

**What was deployed

- Persistent storage for blockchain data
- Resource limits for predictable performance
- Service discovery between components
- Health checks and monitoring ready
- Infrastructure as Code approach

