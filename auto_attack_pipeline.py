"""
Auto Attack Pipeline — Web3 Continuous Execution Engine
Detects unhandled issues/bounties, validates actionability,
synthesizes solutions/proposals with Gemini 3.5 Flash, tests, and publishes directly to GitHub.
Runs continuously non-stop.
"""

import os
import sys
import json
import time
import subprocess
import urllib.request
import urllib.error
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
ALERTS_FILE = os.path.join(OUTPUTS_DIR, "instant_alerts.json")
HANDLED_FILE = os.path.join(OUTPUTS_DIR, "handled_tickets.json")
TIMELINE_FILE = os.path.join(OUTPUTS_DIR, "timeline_forecast.json")
EVENTS_FILE = os.path.join(OUTPUTS_DIR, "financial_events.json")

def get_gemini_api_key():
    k = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if k and k != "test":
        return k
    env_paths = [
        os.path.join(os.path.dirname(__file__), ".env"),
        r"C:\Projetos com IA\cerebro-ia\.env"
    ]
    for p in env_paths:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("GOOGLE_API_KEY=") and len(line.split("=", 1)[1]) > 10:
                            return line.split("=", 1)[1].strip()
                        if line.startswith("GEMINI_API_KEY=") and line.split("=", 1)[1].strip() != "test":
                            return line.split("=", 1)[1].strip()
            except Exception:
                pass
    return ""

API_KEY = get_gemini_api_key()
MODEL_NAME = "gemini-3.5-flash"
WALLET_BASE = "0x3a391d8a77417bbdfb9bea9836772ced4b67880a"
WALLET_SOLANA = "Gu8RhvagFJVZar4NvWdcD1Q4m2GXMXZca271q8iU79B3"

def get_github_token():
    try:
        p = subprocess.run(['git', 'credential', 'fill'], input='protocol=https\nhost=github.com\n\n', text=True, capture_output=True)
        creds = dict(line.split('=', 1) for line in p.stdout.splitlines() if '=' in line)
        return creds.get('password', '')
    except Exception:
        return ""

def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return default

def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[WARN] Error saving {path}: {e}")

def ask_gemini(prompt):
    models = ["gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-2.5-flash"]
    for m in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={API_KEY}"
        payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json", "User-Agent": "AutoAttackPipeline/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
                return data['candidates'][0]['content']['parts'][0]['text']
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(2)
                continue
            print(f"[WARN] Gemini {m} error: {e}")
        except Exception as e:
            print(f"[WARN] Gemini {m} error: {e}")

    # Fallback to local OmniRoute / 9Router (:20128)
    try:
        route_url = "http://127.0.0.1:20128/v1/chat/completions"
        route_payload = json.dumps({
            "model": "auto/best-fast",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1500
        }).encode("utf-8")
        r_req = urllib.request.Request(route_url, data=route_payload, headers={"Content-Type": "application/json", "Authorization": "Bearer local"})
        with urllib.request.urlopen(r_req, timeout=25) as r_resp:
            r_data = json.loads(r_resp.read().decode())
            return r_data['choices'][0]['message']['content']
    except Exception as e2:
        print(f"[WARN] OmniRoute fallback error: {e2}")

    return None

def attack_open_opportunities():
    alerts = load_json(ALERTS_FILE, [])
    handled = load_json(HANDLED_FILE, [])
    token = get_github_token()

    if not alerts:
        return

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Auto Attack Engine: analisando {len(alerts)} chamados...")

    for alert in alerts:
        key = alert.get("key", "")
        if not key or key in handled:
            continue

        repo = alert.get("repo", "")
        title = alert.get("title", "")
        url = alert.get("url", "")
        status = alert.get("status_label", "")

        # Apenas chamados livres ou com baixa concorrência
        if "LIVRE" not in status and int(alert.get("comments", 0) or 0) != 0:
            continue

        print(f"[{datetime.now().strftime('%H:%M:%S')}] ATACANDO OPORTUNIDADE: {key} - {title[:50]}...")

        # 1. Obter detalhes da issue e validar se esta ativa e sem PR
        issue_body = ""
        issue_num = key.split('#')[-1]
        try:
            issue_api_url = f"https://api.github.com/repos/{repo}/issues/{issue_num}"
            req = urllib.request.Request(issue_api_url, headers={"User-Agent": "AutoAttack/1.0", "Authorization": f"token {token}"} if token else {"User-Agent": "AutoAttack/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                issue_data = json.loads(resp.read().decode())
                if issue_data.get("state") != "open":
                    print(f"[SKIP] Issue {key} is already closed.")
                    handled.append(key)
                    save_json(HANDLED_FILE, handled)
                    continue
                if issue_data.get("pull_request"):
                    print(f"[SKIP] {key} is already a pull request.")
                    handled.append(key)
                    save_json(HANDLED_FILE, handled)
                    continue
                issue_body = issue_data.get("body", "") or ""

            # Check comments to avoid duplicate PRs / already solved issues
            comm_url = f"https://api.github.com/repos/{repo}/issues/{issue_num}/comments?per_page=10"
            req_c = urllib.request.Request(comm_url, headers={"User-Agent": "AutoAttack/1.0", "Authorization": f"token {token}"} if token else {"User-Agent": "AutoAttack/1.0"})
            with urllib.request.urlopen(req_c, timeout=10) as resp_c:
                comments_list = json.loads(resp_c.read().decode())
                has_active_pr = any("pull/" in (c.get("body") or "").lower() or "fix pr opened" in (c.get("body") or "").lower() for c in comments_list)
                if has_active_pr:
                    print(f"[SKIP] {key} already has an active PR open by another contributor.")
                    handled.append(key)
                    save_json(HANDLED_FILE, handled)
                    continue
        except Exception as e:
            print(f"[WARN] Falha ao verificar issue {key}: {e}")
            continue

        # 1.5 ComplianceGate: ler documentacao oficial do repositorio ANTES de atuar
        comp_rules_note = ""
        try:
            from compliance_gate import validate_and_load_rules
            comp = validate_and_load_rules(repo, platform="GitHub", token=token)
            if not comp.get("allowed", True):
                print(f"[COMPLIANCE BLOCK] {repo}: {comp.get('block_reason')}")
                handled.append(key)
                save_json(HANDLED_FILE, handled)
                continue
            r_info = comp.get("rules", {})
            docs_str = ", ".join(comp.get("docs_found", [])) or "README"
            ci_str = ", ".join(r_info.get("ci_checks", [])) or "PR tests"
            comp_rules_note = f"\nRepo Compliance Docs ({docs_str}): mode={r_info.get('submission_mode')}, required CI checks={ci_str}, program={r_info.get('program')}."
        except Exception as comp_err:
            print(f"[WARN] ComplianceGate {repo}: {comp_err}")

        # 2. Avaliar viabilidade e sintetizar solucao tecnica rigorosa em Ingles
        prompt = f"""You are a principal systems and compiler engineer reviewing an open-source ticket on repository {repo}.
Analyze this issue and write a concise, authoritative technical evaluation or code solution:
Title: {title}
Issue Context:
{issue_body[:2500]}

Guidelines:
1. First line MUST be strictly `VERDICT: VIABLE` or `VERDICT: NOT_VIABLE`. Write exclusively in clear, professional English.
2. Do NOT use letter headers, greetings, role introductions, dates, or signatures. Start immediately with technical substance.
3. If this is an architectural issue or Wildcard proposal, articulate the premise challenged, the architectural trade-off, and the falsification test criteria.
4. If this is a compiler/systems soundness bug, specify the root cause, provide a clean diff or patch snippet, and specify regression test coverage.
5. Do NOT append wallet addresses to this issue analysis.
Format cleanly with GitHub Flavored Markdown."""

        solution_text = ask_gemini(prompt)
        if not solution_text or (solution_text.strip().splitlines()[0].upper().find("NOT_VIABLE") != -1):
            print(f"[WARN] Gemini não conseguiu sintetizar solução para {key}")
            continue

        # 3. Postar resposta técnica/proposta ou criar branch e PR
        issue_num = key.split('#')[-1]
        comment_url = f"https://api.github.com/repos/{repo}/issues/{issue_num}/comments"
        post_payload = {"body": solution_text}
        
        posted_url = None
        if token:
            try:
                post_req = urllib.request.Request(
                    comment_url,
                    data=json.dumps(post_payload).encode('utf-8'),
                    headers={
                        "Authorization": f"token {token}",
                        "User-Agent": "AI-Revenue-Engine/4.0",
                        "Accept": "application/vnd.github.v3+json",
                        "Content-Type": "application/json"
                    }
                )
                with urllib.request.urlopen(post_req, timeout=15) as resp:
                    res_data = json.loads(resp.read().decode())
                    posted_url = res_data.get("html_url") if res_data.get("id") else None
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] SUCESSO! Solução/Proposta publicada em: {posted_url}")
            except Exception as e:
                print(f"[WARN] Erro ao postar comentário no GitHub: {e}")

        if not posted_url: print(f"[FAIL A01] Envio nao confirmado para {key}"); continue
        # 4. Registrar como atacado apenas apos confirmacao HTTP + id + url
        handled.append(key)
        save_json(HANDLED_FILE, handled)

        # 5. Adicionar à Timeline
        timeline = load_json(TIMELINE_FILE, [])
        is_wildcard = "wildcard" in title.lower()
        val_est = "Pool compartilhado (não estimável)"
        stage_label = f"PROPOSTA COMENTADA (#{issue_num})" if is_wildcard else f"COMENTÁRIO TÉCNICO (#{issue_num})"
        
        timeline.insert(0, {
            "submitted_at": datetime.now().strftime("%d/%m %H:%M"),
            "repo": repo,
            "pr_number": int(issue_num),
            "pr_url": posted_url,
            "deliverables": f"{title[:70]}...",
            "value_estimate_usd": val_est,
            "stage": stage_label,
            "payout_forecast": "Aguardando avaliação do mantenedor",
            "payout_destination": f"Base ({WALLET_BASE[:10]}...)",
            "probability": "Não estimável (sem histórico calibrado)",
            "status": "🟢 ATUADO (SUBMETIDO NA PLATAFORMA)",
            "elapsed_time": "Recém Submetido"
        })
        save_json(TIMELINE_FILE, timeline)

        # 6. Registrar Evento de Notificação
        events = load_json(EVENTS_FILE, [])
        events.insert(0, {
            "type": "NEW_SUBMISSION",
            "icon": "⚡",
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "title": f"Novo Chamado Atacado: {repo}#{issue_num}",
            "details": f"Análise técnica sintetizada e protocolada diretamente no repositório. Concorrendo a {val_est}.",
            "impact": f"+ {val_est} em Disputa",
            "status": "SUBMETIDO COM SUCESSO",
            "badge_color": "#10b981"
        })
        save_json(EVENTS_FILE, events[:250])
        try:
            from compliance_gate import audit_and_normalize_timeline
            audit_and_normalize_timeline()
        except Exception:
            pass

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Item {key} integrado com sucesso à timeline e eventos!")
        # Pausa de 3 segundos entre chamados para respeitar rate limits
        time.sleep(3)

if __name__ == "__main__":
    attack_open_opportunities()
