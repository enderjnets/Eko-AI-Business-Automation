# AGENTS.md — Eko AI Business Automation

> **Agent Protocol:** Every code change must follow the **Commit Trio**.
> 1. **Memory** → Update this file + CHANGELOG.md
> 2. **GitHub** → `git commit` + `git push origin main`
> 3. **Paperclip** → POST `/issues` with `status=done`

---

## Project Overview

**Eko AI Business Automation** — FastAPI backend + Next.js 14 frontend + Tailwind.
Autonomous AI agents for prospecting, outreach, sales, and deal closure for local businesses in Denver, CO.

| | |
|---|---|
| **Backend** | FastAPI + SQLAlchemy (async) + PostgreSQL + Redis + Celery |
| **Frontend** | Next.js 14 (App Router) + Tailwind CSS |
| **AI Provider** | MiniMax M2.7 (primary) + Kimi Code fallback |
| **Email** | Resend (outbound + inbound) |
| **Voice** | VAPI.ai (outbound + inbound assistant "Eva") |
| **Calendar** | Cal.com API v1 (decommissioned — custom `/book-demo` fallback) |
| **Notifications** | Email + Telegram (@EkoBit_Rog_bot) |
| **Observability** | Paperclip (AI Company Control Plane) |

---

## URLs

| Environment | URL |
|---|---|
| Frontend (production) | `https://ender-rog.tail25dc73.ts.net` |
| Backend API | `https://ender-rog.tail25dc73.ts.net/api/v1` |
| Health check | `https://ender-rog.tail25dc73.ts.net/health` |
| Booking page | `https://ender-rog.tail25dc73.ts.net/book-demo` |
| Paperclip UI | `http://100.88.47.99:3100` |

---

## Key Config Values

```python
# Voice
VAPI_INBOUND_PHONE_NUMBER = "+1-256-364-1727"
VAPI_EKO_ASSISTANT_ID = "8c2de53b-3979-4e15-8824-757b749b27c3"

# Notifications
ENDER_NOTIFICATION_EMAIL = "ender@ekoaiautomation.com"
TELEGRAM_BOT_TOKEN = "8264195169:AAG94XS7lPHh_L7DBvTNVKSR_4geB_WEju0"
TELEGRAM_CHAT_ID = "771213858"

# Email
RESEND_FROM_EMAIL = "Eko AI <contact@biz.ekoaiautomation.com>"
RESEND_INBOUND_DOMAIN = "biz.ekoaiautomation.com"
AUTO_REPLY_ENABLED = True

# URLs (production)
APP_URL = "https://ender-rog.tail25dc73.ts.net"
FRONTEND_URL = "https://ender-rog.tail25dc73.ts.net"
ENVIRONMENT = "production"
```

---

## Active Demo / Test Lead

| Field | Value |
|---|---|
| **Business** | X3nails & Spa |
| **Contact** | Margie (margie240478@gmail.com) |
| **Lead ID** | 74 |
| **Status** | `CONTACTED` |
| **Score** | 90/100 (urgency 88, fit 92) |
| **Phone** | +13037162622 |
| **City** | Lakewood, CO |

**Demo flow:** Outreach email → Margie replies → AI auto-reply (booking link + phone) → Margie books demo → Demo happens → Proposal → Close.

---

## Recent Changes (v0.6.1)

See full details in `CHANGELOG.md`.

- VAPI inbound assistant "Eva" with `book_demo` tool
- Resend inbound webhook with AI analysis + auto-reply
- Svix signature verification fix (standardwebhooks lib)
- Public `/book-demo` HTML page
- Demo invite + Ender notification email templates
- Eko Rog Telegram notifier
- Sales brief generator
- Calendar links utility

---

## Docker Workflow

```bash
# After any backend code change
cd Eko-AI-Bussinnes-Automation
docker compose up -d --no-deps backend celery-worker celery-beat

# After any frontend code change
docker compose build --no-cache frontend
docker compose up -d frontend

# Full restart
docker compose up -d
```

**Note:** Frontend has NO volume mount. Must rebuild after every change.

---

## Tailscale Funnel

```bash
# Check status
sudo tailscale funnel status

# Reset and point to backend (port 8000)
sudo tailscale funnel reset
sudo tailscale funnel --bg 8000

# Or point to frontend (port 3001)
sudo tailscale funnel --bg 3001
```

Current: `https://ender-rog.tail25dc73.ts.net/` → `http://127.0.0.1:8000`

---

## Common Commands

```bash
# Reset lead for test
docker exec eko-db psql -U eko -d eko_ai \
  -c "UPDATE leads SET status='DISCOVERED' WHERE id=74; DELETE FROM interactions WHERE lead_id=74;"

# Send outreach email (manual, inside container)
docker exec eko-backend python3 send_outreach.py

# Simulate reply (manual, inside container)
docker exec eko-backend python3 simulate_reply.py

# Check webhook logs
docker logs eko-backend --tail 50 | grep -i webhook
```

---

## Paperclip Commit Trio

```bash
# 1. Git
git add -A
git commit -m "feat: description"
git push origin main

# 2. CHANGELOG
# Edit CHANGELOG.md → add version section

# 3. Paperclip issue
curl -sS "http://100.88.47.99:3100/api/companies/a5151f95-51cd-4d2d-a35b-7d7cb4f4102e/issues" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title":"EKO-N: description","description":"...","priority":"high","status":"done"}'
```

---

*Last updated: 2026-04-29 by Kimi Code CLI (EKO-1754)*
