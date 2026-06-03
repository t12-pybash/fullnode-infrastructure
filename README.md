# Fullnode Infrastructure Engineering

> Production-grade blockchain node infrastructure for the OP Stack ecosystem — built on the operational patterns used to run 20+ blockchain protocols at multi-petabyte scale.

---

## Background

This repository reflects infrastructure engineering patterns developed running production blockchain infrastructure at scale — operating fullnodes across Bitcoin, Ethereum, Solana, Optimism, and 16+ other protocols on AWS and bare metal (OVH, Equinix, Hetzner).

The patterns here — StatefulSet-based node deployment, custom metrics exporters, GitOps delivery, eBPF-based networking — were developed under real production constraints: multi-petabyte chain data, high-availability requirements, and the need to reduce node deployment time from 4 hours to 15 minutes through automation.

This implementation targets the OP Stack (Ethereum L1 + Optimism L2) as a representative case, but the architecture applies directly to any stateful blockchain workload on Kubernetes.

---

## Stack

| Layer | Technology |
|---|---|
| Cloud | AWS EKS (VPC, subnets, IAM, node groups via Terraform) |
| Orchestration | Kubernetes — StatefulSets, Services, ConfigMaps |
| Nodes | Ethereum L1 (execution layer) + OP Stack L2 (Optimism) |
| Networking | Cilium CNI, eBPF-based policy enforcement |
| Monitoring | Prometheus + Grafana + custom blockchain metrics exporter (Python) |
| CI/CD | GitHub Actions (validate → plan → deploy → smoke test) + CircleCI |
| IaC | Terraform ~1.6, `aws` provider ~5.0 |

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   AWS EKS Cluster                  │
│  ┌────────────────┐      ┌─────────────────────┐  │
│  │   L1 Ethereum   │      │    L2 OP Stack       │  │
│  │   StatefulSet   │痄────▚│    StatefulSet       │  │
│  │   Port: 8570   │      │    Port: 9570       │  │
│  └────────┬────────┘      └──────────┬──────────┘  │
│           │                          │              │
│           └──────────┬──────────────┘               │
│                     ▼                              │
│           ┌──────────────────────┐                  │
│           │  Blockchain Metrics  │                  │
│           │  Exporter (Python)   │                  │
│           └──────────┬───────────┘                  │
│                       ▼                              │
│           ┌──────────────────────┐                  │
│           │  Prometheus/Grafana   │                   │
│           └──────────────────────┘                  │
└─────────────────────────────────────────────────────┘
```

**AWS infrastructure (Terraform):**
- VPC with public subnets across 2 AZs
- EKS cluster (Kubernetes 1.27) with managed node group
- IAM roles with least-privilege policies
- Internet Gateway + route tables

---

## CI/CD Pipeline

GitHub Actions runs a 4-stage pipeline on every push to `main`:

| Stage | What it does |
|---|---|
| `terraform-validate` | `init` → `validate` → `plan` |
| `kubernetes-validate` | `kubectl --dry-run` on all manifests |
| `deploy-infrastructure` | Apply Terraform + deploy K8s manifests to EKS |
| `smoke-tests` | Port-forward + curl health checks on node endpoints |

---

## Monitoring

A custom Python **blockchain metrics exporter** scrapes node JSON-RPC endpoints and exposes Prometheus metrics:

- `blockchain_block_height` — current chain tip
- `blockchain_peer_count` — connected peers
- `blockchain_sync_status` — sync progress

Standard node exporters don't understand chain-specific state — a purpose-built exporter is necessary for meaningful blockchain observability. This pattern was extended across 20+ protocols in production with custom metrics per chain (slot timing for Solana, uncle rates for Ethereum, UTXO set size for Bitcoin).

---

## Key Engineering Decisions

**StatefulSets over Deployments** — blockchain nodes require stable network identity and persistent storage for chain data. Pod restarts must preserve volume bindings; StatefulSets guarantee this where Deployments do not.

**Cilium CNI with eBPF network policies** — eBPF-based policy enforcement provides L3/L4 visibility and control without the overhead of iptables chains. In production, this was used to control inter-node peer communication and restrict JSON-RPC exposure to authorised services only.

**Custom metrics exporter** — blockchain sync state, peer connectivity, and chain tip lag are not exposed by any generic exporter. Purpose-built exporters per protocol were the primary mechanism for SLO definition and incident detection in production.

**Modular Terraform** — VPC, EKS, and IAM are separated so each layer can be modified independently without full teardown. This mirrors the pattern used across multi-region bare metal and cloud deployments at scale.

---

## Related Work

- **[homelab-gitops](https://github.com/t12-pybash/homelab-gitops)** — 5-node bare metal k8s cluster with Cilium, GitOps, private AI platform (LiteLLM, Qdrant, Ollama), Prometheus, Falco
- **[sre-cli](https://github.com/t12-pybash/sre-cli)** — custom SRE CLI for Kubernetes: Prometheus alerting, Alertmanager, semantic runbook search via Qdrant

---

*Ciarán Donegan — Lead SRE | [LinkedIn](https://www.linkedin.com/in/cdonegan7/) | [t-12.io](https://t-12.io)*
