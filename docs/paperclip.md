# Paperclip Integration — Eko AI Business Automation

## Overview

Eko AI is registered as a company in **Paperclip** (AI Company Control Plane) for full traceability of agent operations, issue tracking, and multi-agent orchestration.

| | |
|---|---|
| **Company** | Eko AI Business Automation |
| **Prefix** | EKO |
| **Paperclip UI** | http://100.88.47.99:3100 |
| **API Base** | http://100.88.47.99:3100/api |
| **Company ID** | `a5151f95-51cd-4d2d-a35b-7d7cb4f4102e` |

---

## Agents

5 agents operate the project, all connected to **Kimi (Moonshot AI)** via HTTP proxy.

| Agent | Role | Model | Budget | Reports To | ID |
|-------|------|-------|--------|------------|-----|
| **CEO** | Strategic decisions | `kimi-k2-72b` | $200/mo | — | `93f74f56-...` |
| **CTO** | Technical architecture | `kimi-k2.5` | $200/mo | CEO | `6f2a537a-...` |
| **Engineer** | Implementation | `kimi-k2.5` | $150/mo | CTO | `07fa7b52-...` |
| **DevOps** | Infrastructure | `kimi-k2` | $100/mo | CTO | `9833c622-...` |
| **Researcher** | Market analysis | `kimi-k2-thinking` | $150/mo | CEO | `4e1368a9-...` |

### Agent Instructions

Each agent has an `AGENTS.md` file at:
```
~/.paperclip/instances/default/companies/{COMPANY_ID}/agents/{AGENT_ID}/instructions/AGENTS.md
```

---

## Kimi Proxy

Paperclip uses Anthropic API format. Kimi (Moonshot AI) uses OpenAI API format. A proxy translates between them.

- **Proxy URL**: `http://127.0.0.1:18794`
- **Proxy Script**: `~/.paperclip/kimi-proxy.py`
- **Upstream**: `https://api.moonshot.cn/v1`

### Start Proxy

```bash
ssh enderj@10.0.0.240
python3 ~/.paperclip/kimi-proxy.py &
curl http://127.0.0.1:18794/health
```

---

## Event Hooks (Backend)

The backend Python code reports key events to Paperclip automatically:

| Event | Hook | Priority |
|-------|------|----------|
| Discovery complete | `on_discovery_complete()` | low/medium |
| Lead enriched | `on_research_complete()` | score-based |
| Email sent | `on_email_sent()` | medium |
| Email failed | `on_email_error()` | high |
| Pipeline status change | `on_lead_status_change()` | stage-based |
| Campaign launched | `on_campaign_launched()` | medium |
| System alert | `on_system_alert()` | configurable |

See: `backend/app/services/paperclip.py`

---

## API Operations

### List Issues
```bash
curl -sS "http://100.88.47.99:3100/api/companies/a5151f95-51cd-4d2d-a35b-7d7cb4f4102e/issues?limit=20" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY"
```

### Create Issue
```python
import requests

requests.post(
    "http://100.88.47.99:3100/api/companies/a5151f95-51cd-4d2d-a35b-7d7cb4f4102e/issues",
    json={
        "title": "EKO-N: description",
        "description": "## Context\n...",
        "priority": "high",  # critical | high | medium | low
        "status": "todo",    # todo | in_progress | in_review | done | cancelled
    },
    headers={"Authorization": f"Bearer {PAPERCLIP_API_KEY}"},
)
```

---

## Commit Trio Protocol

Every code change follows the **commit trio**:

1. **Code change** → git commit + push
2. **Version bump** → update changelog
3. **Paperclip issue** → POST `/issues` with `status=done`

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Connection refused :18794` | Start Kimi proxy: `python3 ~/.paperclip/kimi-proxy.py` |
| `Agent key cannot access another company` | Use board key (`pcp_board_...`) |
| `Invalid enum value` for priority | Use: `critical`, `high`, `medium`, `low` (not `urgent`) |
