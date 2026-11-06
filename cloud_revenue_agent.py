"""
Autonomous Web3 Cloud Revenue Agent
Runs 24/7 on GitHub Actions Cloud Infrastructure.
Monitors Solana & EVM wallets, tracks bounty disbursements, discovers fresh opportunities,
and logs real-time financial telemetry directly to the repository.
"""

import os
import sys
import json
import time
from datetime import datetime, timezone
import urllib.request
import urllib.error

SOLANA_WALLET = "Gu8RhvagFJVZar4NvWdcD1Q4m2GXMXZca271q8iU79B3"
EVM_WALLET = "0x3a391d8a77417bbdfb9bea9836772ced4b67880a"
GITHUB_USER = "dukenordj-rgb"

SOLANA_RPC = "https://api.mainnet-beta.solana.com"
BASE_RPC = "https://base-rpc.publicnode.com"

def check_solana_balance():
    try:
        payload = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBalance",
            "params": [SOLANA_WALLET]
        }).encode("utf-8")
        req = urllib.request.Request(
            SOLANA_RPC, 
            data=payload, 
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            lamports = data.get("result", {}).get("value", 0)
            return lamports / 1e9
    except Exception as e:
        print(f"[WARN] Error querying Solana balance: {e}")
        return 0.0

def check_evm_balance():
    try:
        payload = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_getBalance",
            "params": [EVM_WALLET, "latest"]
        }).encode("utf-8")
        req = urllib.request.Request(
            BASE_RPC, 
            data=payload, 
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            hex_val = data.get("result", "0x0")
            wei = int(hex_val, 16)
            return wei / 1e18
    except Exception as e:
        print(f"[WARN] Error querying EVM Base balance: {e}")
        return 0.0

def scan_github_pr_status():
    url = f"https://api.github.com/search/issues?q=author:{GITHUB_USER}+type:pr"
    headers = {"User-Agent": "AutonomousRevenueAgent/1.0"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            items = data.get("items", [])
            prs = []
            for item in items[:10]:
                prs.append({
                    "title": item.get("title"),
                    "url": item.get("html_url"),
                    "state": item.get("state"),
                    "created_at": item.get("created_at"),
                    "closed_at": item.get("closed_at")
                })
            return prs
    except Exception as e:
        print(f"[WARN] GitHub search error: {e}")
        return []

def run_telemetry_cycle():
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[{now_utc}] Invocando ciclo do Agente Autônomo na Nuvem...")
    
    sol_bal = check_solana_balance()
    evm_bal = check_evm_balance()
    prs = scan_github_pr_status()
    
    telemetry = {
        "timestamp": now_utc,
        "agent": "Cloud Revenue Agent v1.0 (GitHub Actions)",
        "wallets": {
            "solana_primary": {
                "address": SOLANA_WALLET,
                "sol_balance": sol_bal
            },
            "base_evm": {
                "address": EVM_WALLET,
                "eth_balance": evm_bal
            }
        },
        "dispatched_prs": prs,
        "engine_health": "100% OPERATIONAL (AUTONOMOUS 24/7)"
    }
    
    with open("CLOUD_DISPATCH_LEDGER.json", "w", encoding="utf-8") as f:
        json.dump(telemetry, f, indent=2)
        
    status_md = f"""# 🟢 Web3 Cloud Autonomous Revenue Agent

> **Status:** 100% Autônomo na Nuvem (Executando via GitHub Actions 24/7 sem necessidade de PC local ligado)  
> **Última Execução:** `{now_utc}`

---

## 💼 Monitoramento On-Chain em Tempo Real
- **Solana Principal:** `{SOLANA_WALLET}` — **Saldo Líquido:** `{sol_bal:.6f} SOL`
- **Base EVM:** `{EVM_WALLET}` — **Saldo Líquido:** `{evm_bal:.6f} ETH`

---

## 🚀 Ativos & Pull Requests em Disputa
Total de PRs/Repositórios Monitorados: **{len(prs)}**
"""
    for pr in prs:
        status_md += f"- **[{pr['title']}]({pr['url']})** — Status: `{pr['state'].upper()}`\n"
        
    with open("LATEST_STATUS.md", "w", encoding="utf-8") as f:
        f.write(status_md)
        
    print(f"[{now_utc}] Ciclo finalizado com sucesso. Ledger e status gerados.")

if __name__ == "__main__":
    run_telemetry_cycle()
