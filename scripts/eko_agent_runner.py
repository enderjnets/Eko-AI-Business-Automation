#!/usr/bin/env python3
"""
EKO Agent Runner for Paperclip
Routes issues to appropriate handlers and uses Kimi proxy for LLM calls.
"""
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone

PAPERCLIP_API = os.environ.get("PAPERCLIP_API_URL", "http://100.88.47.99:3100")
COMPANY_ID = "a5151f95-51cd-4d2d-a35b-7d7cb4f4102e"
AGENT_ID = os.environ.get("PAPERCLIP_AGENT_ID", "")
RUN_ID = os.environ.get("PAPERCLIP_RUN_ID", "")
API_KEY = os.environ.get(
    "PAPERCLIP_API_KEY",
    "pcp_board_68ed2bc4520167360cb1ae178b2b3285692f536e08aa7300",
)
KIMI_PROXY_URL = "http://127.0.0.1:18794/v1/messages"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

AGENT_ID_TO_ROLE = {
    "93f74f56-11b7-4368-9ae8-a842d1bdb766": "ceo",
    "6f2a537a-5dd0-4b88-8b1a-b63272323cca": "cto",
    "4e1368a9-92d7-4d75-8d8b-b5fc1925ff69": "researcher",
    "9833c622-2045-4cfd-adad-b9cc80a940b5": "devops",
    "07fa7b52-03f7-4a29-b2ca-ac62909ae523": "engineer",
}

AGENT_ID_TO_NAME = {
    "93f74f56-11b7-4368-9ae8-a842d1bdb766": "CEO",
    "6f2a537a-5dd0-4b88-8b1a-b63272323cca": "CTO",
    "4e1368a9-92d7-4d75-8d8b-b5fc1925ff69": "Researcher",
    "9833c622-2045-4cfd-adad-b9cc80a940b5": "DevOps",
    "07fa7b52-03f7-4a29-b2ca-ac62909ae523": "Engineer",
}

AGENT_ID_TO_MODEL = {
    "93f74f56-11b7-4368-9ae8-a842d1bdb766": "kimi-k2-72b",
    "6f2a537a-5dd0-4b88-8b1a-b63272323cca": "kimi-k2.5",
    "4e1368a9-92d7-4d75-8d8b-b5fc1925ff69": "kimi-k2-thinking",
    "9833c622-2045-4cfd-adad-b9cc80a940b5": "kimi-k2",
    "07fa7b52-03f7-4a29-b2ca-ac62909ae523": "kimi-k2.6",
}


def log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    name = AGENT_ID_TO_NAME.get(AGENT_ID, "Unknown")
    line = f"[{ts}] [{level}] [{name}] {msg}"
    print(line, flush=True)


def api_request(path: str, method: str = "GET", data: dict = None) -> dict:
    url = f"{PAPERCLIP_API}{path}"
    req = urllib.request.Request(url, headers=HEADERS, method=method)
    if data:
        req.data = json.dumps(data).encode()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        log(f"API error {e.code}: {e.read().decode()[:200]}", "ERROR")
        return {}
    except Exception as e:
        log(f"API exception: {e}", "ERROR")
        return {}


def call_kimi(prompt: str, system: str = "", max_tokens: int = 2000) -> str:
    """Call Kimi via local proxy."""
    try:
        model = AGENT_ID_TO_MODEL.get(AGENT_ID, "kimi-k2-72b")
        req_body = {
            "model": model,
            "messages": [
                {"role": "user", "content": f"{system}\n\n{prompt}"} if system else {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7,
        }
        req = urllib.request.Request(
            KIMI_PROXY_URL,
            data=json.dumps(req_body).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            if "content" in result:
                for block in result["content"]:
                    if block.get("type") == "text":
                        return block.get("text", "")
            return str(result)
    except Exception as e:
        log(f"Kimi call failed: {e}", "WARN")
        return None


def get_my_issues() -> list:
    if not AGENT_ID:
        log("PAPERCLIP_AGENT_ID not set", "ERROR")
        return []
    result = api_request(
        f"/api/companies/{COMPANY_ID}/issues?status=todo&assigneeAgentId={AGENT_ID}"
    )
    issues = result if isinstance(result, list) else result.get("items", [])
    log(f"Found {len(issues)} todo issues")
    return issues


def checkout_issue(issue_id: str) -> bool:
    result = api_request(
        f"/api/issues/{issue_id}/checkout",
        method="POST",
        data={"agentId": AGENT_ID, "expectedStatuses": ["todo", "backlog", "blocked", "in_review"]},
    )
    if isinstance(result, dict) and result.get("error"):
        log(f"Checkout failed: {result['error']}", "WARN")
        return False
    return True


def add_comment(issue_id: str, body: str) -> None:
    api_request(
        f"/api/issues/{issue_id}/comments",
        method="POST",
        data={"body": body},
    )


def set_status(issue_id: str, status: str) -> None:
    api_request(
        f"/api/issues/{issue_id}",
        method="PATCH",
        data={"status": status},
    )


def process_issue(issue: dict) -> dict:
    issue_id = issue["id"]
    title = issue.get("title", "")
    desc = issue.get("description", "")
    
    role = AGENT_ID_TO_ROLE.get(AGENT_ID, "unknown")
    name = AGENT_ID_TO_NAME.get(AGENT_ID, "Agent")
    
    if not checkout_issue(issue_id):
        return {"status": "skipped", "summary": "checkout failed"}
    
    log(f"Processing {issue.get('identifier', issue_id)}: {title[:60]}")
    
    # Build prompt for Kimi
    system = f"You are the {name} ({role}) of EKO AI Business Automation. You help with lead discovery, research, outreach, and CRM management."
    prompt = f"Issue: {title}\n\nDescription:\n{desc}\n\nWhat action should I take? Provide a concise response with clear next steps."
    
    response = call_kimi(prompt, system, max_tokens=1500)
    
    if response:
        comment = f"🤖 **{name}** processed this issue using Kimi ({AGENT_ID_TO_MODEL.get(AGENT_ID, 'default')}).\n\n**Analysis:**\n{response}\n\n---\n*Run ID: {RUN_ID[:16] if RUN_ID else 'N/A'}*"
        add_comment(issue_id, comment)
        set_status(issue_id, "done")
        log(f"Completed with Kimi response ({len(response)} chars)")
        return {"status": "fixed", "summary": f"processed with Kimi ({len(response)} chars)"}
    else:
        add_comment(issue_id, f"⚠️ {name} attempted to process but Kimi proxy returned an error. Manual review needed.")
        log("Kimi returned no response", "WARN")
        return {"status": "escalate", "summary": "Kimi proxy error"}


def main():
    log(f"=== EKO Agent Runner Started ===")
    
    if not AGENT_ID:
        log("PAPERCLIP_AGENT_ID not set", "ERROR")
        sys.exit(1)
    
    name = AGENT_ID_TO_NAME.get(AGENT_ID, "Unknown")
    role = AGENT_ID_TO_ROLE.get(AGENT_ID, "unknown")
    model = AGENT_ID_TO_MODEL.get(AGENT_ID, "default")
    log(f"Agent: {name} (role={role}, model={model})")
    
    # Test Kimi proxy
    try:
        req = urllib.request.Request("http://127.0.0.1:18794/health")
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                log("Kimi proxy: OK")
            else:
                log(f"Kimi proxy: status {resp.status}", "WARN")
    except Exception as e:
        log(f"Kimi proxy unreachable: {e}", "WARN")
    
    issues = get_my_issues()
    if not issues:
        log("No work to do — exiting cleanly")
        sys.exit(0)
    
    processed = 0
    for issue in issues:
        result = process_issue(issue)
        if result.get("status") != "skipped":
            processed += 1
        time.sleep(1)
    
    log(f"=== Runner Complete — processed {processed}/{len(issues)} issues ===")
    sys.exit(0)


if __name__ == "__main__":
    main()
