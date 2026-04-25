# Fullnode Infrastructure Engineering

> Production-grade blockchain node infrastructure for the OP Stack ecosystem — Kubernetes, Terraform (AWS EKS), custom Prometheus metrics, and a full CI/CD deployment pipeline.

---

## Overview

This project provisions and operates an **Optimism (OP Stack) L1/L2 blockchain node environment**, covering everything from cloud infrastructure through to application-layer monitoring. It demonstrates the full lifecycle of infrastructure engineering: provisioning, deployment, observability, and automated delivery.

**Stack:**
- **Cloud:** AWS EKS (VPC, subnets, IAM, node groups via Terraform)
- **Orchestration:** Kubernetes — StatefulSets, Services, ConfigMaps, Namespaces
- **Nodes:** Ethereum L1 (execution layer) + OP Stack L2 (Optimism)
- **Monitoring:** Prometheus + Grafana + custom blockchain metrics exporter (Python)
- **CI/CD:** GitHub Actions (validate → plan → deploy → smoke test) + CircleCI
- **IaC:** Terraform ~1.6, `aws` provider ~5.0

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    AWS EKS Cluster                  │
│  ┌─────────────────┐      ┌─────────────────────┐  │
│  │   L1 Ethereum   │      │    L2 OP Stack       │  │
│  │   StatefulSet   │◄────►│    StatefulSet       │  │
│  │   Port: 8570    │      │    Port: 9570        │  │
│  └────────┬────────┘      └──────────┬──────────┘  │
│           │                          │              │
│           └──────────┬───────────────┘              │
│                      ▼                              │
│           ┌──────────────────────┐                  │
│           │  Blockchain Metrics  │                  │
│           │  Exporter (Python)   │                  │
│           └──────────┬───────────┘                  │
│                      ▼                              │
│           ┌──────────────────────┐                  │
│           │  Prometheus/Grafana  │                  │
│           │  (monitoring stack)  │                  │
│           └──────────────────────┘                  │
└─────────────────────────────────────────────────────┘
```

**AWS infrastructure (Terraform):**
- VPC with public subnets across 2 AZs
- EKS cluster (Kubernetes 1.27) with managed node group (t3.medium)
- IAM roles: cluster role + worker node role with least-privilege policies
- Internet Gateway + route tables for node communication

---

## Repository Structure

```
.
├── infrastructure/
│   ├── kubernetes/          # K8s manifests (StatefulSets, Services, ConfigMaps)
│   ├── monitoring/          # Prometheus + Grafana + custom exporter
│   └── terraform/aws-eks/   # EKS cluster, VPC, IAM via Terraform
├── scripts/                 # Setup and validation scripts
├── docs/                    # Setup guide
├── blockchain-live-monitor.py   # Real-time node monitoring script
├── blockchain-metrics-*.yaml   # Prometheus scrape configs
├── l1-ethereum-simple.yaml      # Simplified L1 node manifest
└── justfile                     # Task runner
```

---

## CI/CD Pipeline

GitHub Actions runs a 4-stage pipeline on every push to `main` that touches `infrastructure/`:

| Stage | What it does |
|---|---|
| `terraform-validate` | `init` → `validate` → `plan` |
| `kubernetes-validate` | `kubectl --dry-run` on all manifests |
| `deploy-infrastructure` | Apply Terraform + deploy K8s manifests to EKS |
| `smoke-tests` | Port-forward + curl health checks on blockchain endpoints |

CircleCI provides a parallel pipeline for infrastructure validation and deployment orchestration.

---

## Monitoring

A custom Python **blockchain metrics exporter** scrapes node JSON-RPC endpoints and exposes Prometheus metrics:

- `blockchain_block_height` — current chain tip
- `blockchain_peer_count` — connected peers
- `blockchain_sync_status` — sync progress

Grafana dashboards visualise chain health across L1 and L2 nodes.

---

## Key Engineering Decisions

- **StatefulSets over Deployments** — blockchain nodes require stable network identity and persistent storage for chain data
- **NodePort services** — external access for JSON-RPC without an ALB (cost-optimised for lab/demo use)
- **Modular Terraform** — VPC, EKS, and IAM separated so each can be changed independently
- **Custom exporter** — standard node exporters do not understand blockchain-specific metrics; a purpose-built Python exporter bridges that gap

---

## Related

- Monitoring and Grafana config: `infrastructure/monitoring/`
- Kubernetes manifests: `infrastructure/kubernetes/`
- Terraform (AWS EKS): `infrastructure/terraform/aws-eks/`

---

*Built as part of a broader infrastructure engineering portfolio. See [t-12.io](https://t-12.io) for more.*
