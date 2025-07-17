#!/usr/bin/env python3
import requests
import time
import json
import subprocess
from datetime import datetime

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return "Error"

def get_blockchain_status():
    print("🚀 OP Stack Infrastructure Engineering Portfolio")
    print("=" * 55)
    print(f"Demo Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Show Kubernetes Infrastructure
    print("📊 Kubernetes Infrastructure Status:")
    print("-" * 35)
    pods_output = run_command("kubectl get pods -n op-stack --no-headers")
    for line in pods_output.split('\n'):
        if line.strip():
            parts = line.split()
            name = parts[0]
            status = parts[2]
            age = parts[4]
            if 'l1-ethereum' in name:
                print(f"   🔗 L1 Ethereum Node:     {status:15} (Age: {age})")
            elif 'l2-opstack' in name:
                print(f"   ⚡ L2 OP Stack Node:     {status:15} (Age: {age})")
            elif 'prometheus' in name:
                print(f"   📊 Prometheus Monitor:   {status:15} (Age: {age})")
            elif 'grafana' in name:
                print(f"   📈 Grafana Dashboard:    {status:15} (Age: {age})")
    print()
    
    # Test Live Blockchain RPCs
    print("🔗 Live Blockchain Node Status:")
    print("-" * 32)
    
    endpoints = {
        'L1 Ethereum': 'http://localhost:8570',
        'L2 OP Stack': 'http://localhost:9570'
    }
    
    for name, url in endpoints.items():
        try:
            payload = {'jsonrpc': '2.0', 'method': 'eth_blockNumber', 'params': [], 'id': 1}
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                result = response.json()
                if 'result' in result:
                    height = int(result['result'], 16)
                    print(f"   {name:12}: ✅ Block {height:,} (Active)")
                else:
                    print(f"   {name:12}: ⚠️  RPC responding, no blocks")
            else:
                print(f"   {name:12}: ❌ HTTP {response.status_code}")
        except Exception as e:
            print(f"   {name:12}: ❌ Connection failed")
    
    print()
    
    # Show Infrastructure Achievements
    print("🏆 Infrastructure Engineering Achievements:")
    print("-" * 43)
    print("   ✅ 53+ hours continuous blockchain operation")
    print("   ✅ Kubernetes StatefulSets with persistent storage")
    print("   ✅ CI/CD pipeline with automated testing")
    print("   ✅ Monitoring stack (Prometheus + Grafana)")
    print("   ✅ Infrastructure as Code (Terraform + AWS)")
    print("   ✅ Professional GitHub portfolio")
    print()
    
    # Show Access URLs
    print("🌐 Infrastructure Access Points:")
    print("-" * 31)
    print("   L1 Ethereum RPC:  http://localhost:8570")
    print("   L2 OP Stack RPC:  http://localhost:9570")
    print("   Prometheus:       http://localhost:9090")
    print("   Grafana:          http://localhost:3000")
    print("   GitHub Portfolio: https://github.com/t12-pybash/op-stack-interview-prep")
    print()
    
    # Show Technical Details
    print("⚙️  Technical Implementation:")
    print("-" * 29)
    print("   • Docker containerization for development")
    print("   • Kubernetes orchestration for production")
    print("   • StatefulSets for persistent blockchain data")
    print("   • NodePort services for external access")
    print("   • ConfigMaps for environment configuration")
    print("   • GitHub Actions for CI/CD automation")
    print("   • Prometheus for metrics collection")
    print("   • Grafana for visualization dashboards")
    print()
    
    print("🎯 READY FOR OPTIMISM INFRASTRUCTURE ENGINEER INTERVIEW!")
    print("=" * 55)

if __name__ == '__main__':
    get_blockchain_status()
