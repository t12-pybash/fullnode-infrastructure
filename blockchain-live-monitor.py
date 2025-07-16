#!/usr/bin/env python3
import requests
import time
from datetime import datetime

def monitor_blockchains():
    print("🚀 OP Stack Live Blockchain Monitor")
    print("=" * 40)
    
    endpoints = {
        'L1 Ethereum': 'http://localhost:8570',
        'L2 OP Stack': 'http://localhost:9570'
    }
    
    try:
        while True:
            print(f"\n📊 {datetime.now().strftime('%H:%M:%S')} - Block Heights:")
            print("-" * 35)
            
            for name, url in endpoints.items():
                try:
                    payload = {'jsonrpc': '2.0', 'method': 'eth_blockNumber', 'params': [], 'id': 1}
                    response = requests.post(url, json=payload, timeout=5)
                    if response.status_code == 200:
                        result = response.json()
                        if 'result' in result:
                            height = int(result['result'], 16)
                            print(f"   {name:12}: Block {height:,}")
                        else:
                            print(f"   {name:12}: No blocks")
                    else:
                        print(f"   {name:12}: HTTP {response.status_code}")
                except Exception as e:
                    print(f"   {name:12}: Connection failed")
            
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n\n✅ Monitoring stopped")

if __name__ == '__main__':
    monitor_blockchains()
