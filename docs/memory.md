# Project Memory — Eko AI Business Automation

**Last updated**: 2026-04-24  
**Current version**: 0.2.0  
**Current phase**: Fase 1 ✅ Complete

---

## What was done (this session)

### Fase 1: Discovery + Research + Dashboard — COMPLETED

#### Code changes
- **4 new discovery sources**: Google Maps, Yelp, LinkedIn (Apify), Colorado SOS (Socrata API)
- **Semantic search**: pgvector + OpenAI embeddings endpoint + auto-generation
- **Frontend improvements**: Source toggles, semantic search mode, removed reload anti-pattern
- **CORS**: Configurable via `CORS_ORIGINS` env var
- **Tests**: `test_discovery.py` + `test_research.py`

#### Infra changes
- `beautifulsoup4` added to requirements
- `ApifyClient` service created
- `CHANGELOG.md` created
- Version bumped: 0.1.0 → 0.2.0

#### Git
- Commits: `1c26f04`, `b9f0de5`
- Pushed to `origin/main`

#### Paperclip
- Issue **EKO-11** created: `Fase 1 Complete — Discovery + Research + Dashboard`
- Status: `done`

---

## Known issues / next steps

### Blockers for production
| Item | Status | Notes |
|------|--------|-------|
| Yelp scraping | ❌ Blocked | Cloudflare 403. Needs Yelp Fusion API key or Apify actor debug |
| LinkedIn actor | ⚠️ Unvalidated | Apify actor exists but input schema not confirmed |
| Outscraper key | ❓ Unknown | Google Maps source assumed OK but not tested live |
| Docker | ⚠️ Down | Colima/Docker Desktop not running locally |
| pytest | ⚠️ Blocked | Python 3.14 incompatible with pydantic-core wheels |

### Next priorities (Fase 2)
1. Fix Yelp (get Yelp Fusion API key → implement native client)
2. Validate LinkedIn Apify actor input
3. Implement Celery scheduled tasks (currently all `pass` stubs)
4. Add SMS/Voice outreach channels
5. Authentication system (JWT)

---

## Environment

### API Keys configured locally
- `APIFY_API_KEY`: ✅ Configured in `.env`
- `PAPERCLIP_API_KEY`: ✅ Configured in `.env`
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
