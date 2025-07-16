#!/usr/bin/env python3
import requests
import time
import json
from prometheus_client import start_http_server, Gauge, Counter
import logging

# Prometheus metrics
block_height = Gauge('blockchain_block_height', 'Current block height', ['chain', 'node'])
rpc_requests = Counter('blockchain_rpc_requests_total', 'Total RPC requests', ['chain', 'method', 'status'])
node_sync_status = Gauge('blockchain_node_syncing', 'Node sync status (1=syncing, 0=synced)', ['chain', 'node'])

# RPC endpoints
ENDPOINTS = {
    'l1-ethereum': 'http://l1-ethereum-service:8545',
    'l2-opstack': 'http://l2-opstack-service:8545'
}

def get_block_height(endpoint, chain):
    try:
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_blockNumber",
            "params": [],
            "id": 1
        }
        
        response = requests.post(endpoint, json=payload, timeout=5)
        rpc_requests.labels(chain=chain, method='eth_blockNumber', status='success').inc()
        
        if response.status_code == 200:
            result = response.json()
            if 'result' in result:
                height = int(result['result'], 16)  # Convert hex to decimal
                return height
        
        rpc_requests.labels(chain=chain, method='eth_blockNumber', status='error').inc()
        return None
        
    except Exception as e:
        logging.error(f"Error getting block height for {chain}: {e}")
        rpc_requests.labels(chain=chain, method='eth_blockNumber', status='error').inc()
        return None

def get_sync_status(endpoint, chain):
    try:
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_syncing",
            "params": [],
            "id": 2
        }
        
        response = requests.post(endpoint, json=payload, timeout=5)
        if response.status_code == 200:
            result = response.json()
            if 'result' in result:
                # eth_syncing returns false when synced, or sync object when syncing
                is_syncing = 1 if result['result'] != False else 0
                return is_syncing
        return 0
        
    except Exception as e:
        logging.error(f"Error getting sync status for {chain}: {e}")
        return 0

def collect_metrics():
    while True:
        for chain, endpoint in ENDPOINTS.items():
            # Get block height
            height = get_block_height(endpoint, chain)
            if height is not None:
                block_height.labels(chain=chain, node=chain).set(height)
                print(f"{chain} block height: {height}")
            
            # Get sync status
            sync_status = get_sync_status(endpoint, chain)
            node_sync_status.labels(chain=chain, node=chain).set(sync_status)
            
        time.sleep(10)  # Collect every 10 seconds

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_http_server(8080)  # Prometheus metrics endpoint
    print("Blockchain metrics exporter started on port 8080")
    collect_metrics()
