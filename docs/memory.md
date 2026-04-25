# Project Memory — Eko AI Business Automation

**Last updated**: 2026-04-24  
**Current version**: 0.4.0  
**Current phase**: Auth ✅ Complete

---

## What was done (this session)

### Auth System: JWT + Protected Routes + Multi-tenancy — COMPLETED

#### Backend
- **User model** with roles: `admin`, `manager`, `agent`
- **JWT security**: bcrypt passwords, access/refresh tokens, `get_current_user`, `get_current_admin`
- **Auth router**: login, register (admin-only), refresh, me, dev-login
- **Protected routes**: All APIs now require Bearer token
- **Multi-tenancy**: Non-admin users only see their own leads; `owner_id` auto-assigned

#### Frontend
- **Auth context**: login state, auto-redirect, localStorage tokens
- **Login page**: email/password + dev login button
- **API client**: Axios interceptors inject Bearer token; auto-redirect on 401
- **Navbar**: shows user name/role + logout

#### Tests
- `tests/test_auth.py` — Password hashing, JWT, RBAC, router endpoints

#### Git
- Version bumped: 0.3.0 → 0.4.0
- CHANGELOG.md updated

#### Paperclip
- Issue **EKO-17** created: `Auth System — JWT + Protected Routes + Multi-tenancy`
- Status: `done`

---

## Previous phases

### Fase 2: Email Outreach + CRM Pipeline + Sequences — COMPLETED
- 4 Celery scheduled tasks implemented
- Email Sequences (drip campaigns) with models, API, dry-run

### Fase 1: Discovery + Research + Dashboard — COMPLETED
- 4 discovery sources, semantic search, multi-source UI

---

## Known issues / next steps

### Blockers for production
| Item | Status | Notes |
|------|--------|-------|
| Colorado SOS | ✅ Working | Official Open Data API |
| Yelp Fusion | ✅ Working | 500 req/day free tier |
| LinkedIn (SerpApi) | ✅ Working | 100 searches/month free tier |
| Auth system | ✅ Working | JWT + RBAC + protected routes |
| Google Maps | ⏳ Deferred | Outscraper requires payment |
| Docker | ⚠️ Down | Colima/Docker Desktop not running locally |
| pytest | ⚠️ Blocked | Python 3.14 incompatible with pydantic-core wheels |
| OpenAI API Key | ❌ Placeholder | Required for enrichment, embeddings, AI email gen |
| Resend API Key | ❌ Placeholder | Required for actual email delivery |

### Next priorities (Fase 3)
1. Voice AI integration (Retell / Vapi)
2. Calendar integration (Cal.com webhooks already exist)
3. Production deployment hardening

---

## Environment

### API Keys configured locally
- `APIFY_API_KEY`: ✅ Configured in `.env`
- `PAPERCLIP_API_KEY`: ✅ Configured in `.env`
- `YELP_API_KEY`: ✅ Configured (free tier)
- `SERPAPI_API_KEY`: ✅ Configured (100 searches/month free)
- `OUTSCRAPER_API_KEY`: ❌ Not configured
- `OPENAI_API_KEY`: ❌ Not configured
- `RESEND_API_KEY`: ❌ Not configured

### Services status
| Service | URL | Status |
|---------|-----|--------|
| Paperclip UI | http://100.88.47.99:3100 | ✅ Online |
| Paperclip API | http://100.88.47.99:3100/api | ✅ Online |
| Eko Backend | http://localhost:8000 | ❌ Not running |
| Eko Frontend | http://localhost:3000 | ❌ Not running |
| PostgreSQL | localhost:5432 | ❌ Not running |
| Redis | localhost:6379 | ❌ Not running |

---

## Quick commands

```bash
# Start Docker infrastructure
colima start  # or Docker Desktop
cd ~/Eko-AI-Bussinnes-Automation
docker-compose up -d

# Verify
curl http://localhost:8000/health

# Run tests (inside Docker or after deps installed)
cd backend && pytest tests/ -v
```
