# Project Memory — Eko AI Business Automation

**Last updated**: 2026-04-25  
**Current version**: 0.6.1  
**Current phase**: Pipeline Fix + Complete Visibility ✅ Complete

---

## What was done (this session)

### v0.6.0 — Enrichment Pipeline Hardening — COMPLETED

#### Backend
- **Celery worker fix** — Resolved `InvalidRequestError: expression 'User' failed to locate a name` by creating `app/models/__init__.py` and importing all models in `celery_app.py`
- **Commit-per-lead** — Both `enrich_pending_leads` scheduled task and `enrich-all` endpoint now commit after each lead instead of batch-end, so UI sees real-time progress
- **Kimi JSON parsing** — Replaced greedy regex with robust `_extract_json()`: direct parse fast path → markdown code block stripping → brace counting with string/escape awareness. Eliminates 50/50 fallback scores from truncated JSON
- **WebsiteFinder hardening** — Blocks `.pdf`, `.gov/`, `.mil/` URLs to prevent wasting enrichment cycles on irrelevant sites
- **Yelp pagination** — Added offset pagination so requesting 200 results correctly makes multiple API calls (50 per call) instead of capping at 50
- **Discovery deduplication** — Fixed `AttributeError: 'NoneType'` when LinkedIn/CO SOS return leads with null city/business_name
- **DiscoveryResponse schema** — Created `DiscoveryResponse` (total_found, new_leads, duplicates_skipped, items) and updated `/discover` endpoint to fix 500 validation error
- **Cal.com auth fix** — Switched from Bearer token to query param (`?apiKey=`) for Cal.com API compatibility
- **Email unsubscribe URL** — Fixed hardcoded `localhost` unsubscribe link in email templates
- **AI client** — Hardened Kimi `json_mode` prompting with explicit "ONLY valid JSON" instruction
- **Docker Compose** — Added `KIMI_API_KEY`, `KIMI_BASE_URL`, `KIMI_MODEL` to all services

#### Frontend
- **Leads pagination** — Added `page` state + Previous/Next buttons, shows 100 per page
- **Enrichment progress bar** — Added to `/leads` page with polling every 10s. Shows processed/pending counts + percentage
- **Discovery dropdowns** — Converted city, state, max_results in `DiscoveryForm` to `<select>` menus with 30 CO cities, 50 US states, and options 10/25/50/100/200
- **Discovery fetch()** — Replaced axios with native `fetch` for `/discover` POST to fix "Network Error" when selecting multiple sources (axios preflight CORS bug)
- **API URL consistency** — Replaced hardcoded `http://10.0.0.240:8001` fetch calls with relative `/api/v1/...` paths (uses Next.js rewrites)

#### Database Snapshot (v0.6.0)
| Status | Count |
|--------|-------|
| DISCOVERED | 400 |
| ENRICHED | 8 |
| SCORED | 72 |
| **Total** | **480** |

Celery worker actively processing 20 leads every 30 minutes.

#### Paperclip
- Issue **EKO-19** created: `v0.6.0 — Enrichment Pipeline Hardening`
- Issue **EKO-410** created: `Pipeline Fix — Complete Visibility + Valid Transitions + Interaction Tracking`
- Issue **EKO-461** created: `Pipeline Empty Kanban Fix — page_size + corrupt email validation`
- Status: `done`

---

### Pipeline Fix — COMPLETED

#### Problems Found
1. **3 missing stages in Kanban** (`active`, `at_risk`, `churned`) — leads disappeared after `closed_won` → `active`
2. **Broken backward arrows** — frontend assumed index-1 was always valid, backend rejected most backward moves silently
3. **Score 0 treated as missing** — defunct businesses (0/0) stuck in `ENRICHED` forever due to Python truthiness
4. **PATCH `/leads/{id}` bypass** — could jump `discovered` → `closed_won` without any pipeline validation
5. **No Interaction records** for CRM emails — broken audit trail and rate limiter
6. **Rate limiter counted inbound emails** — lead clicks/openings blocked outreach

#### Backend Fixes
- Score 0 is valid: `is not None` instead of truthiness (3 places: `scheduled.py`, `leads.py` ×2)
- `update_lead` PATCH now validates transitions via `VALID_TRANSITIONS` + records Interaction
- Rate limiter filters `direction="outbound"` only
- `contact_lead` creates `Interaction` record with metadata (template, AI-generated, message_id)

#### Frontend Fixes (KanbanBoard)
- 13 complete stages including `active`/`at_risk`/`churned`
- Arrows only show **valid transitions** (mirrors backend `VALID_TRANSITIONS`)
- Load all leads without 100/page limit
- Alert on invalid transition instead of silent `console.error`

---

### Pipeline Empty Kanban Fix — COMPLETED

#### Problem
Pipeline Kanban was completely empty — no leads visible in any stage.

#### Root Causes
1. **page_size mismatch** — KanbanBoard requested `page_size=9999` but backend limited to `le=100`. API returned 422 validation error.
2. **Corrupt email data** — Some discovery sources (CO SOS/Yelp) produced invalid emails like `K@48G9-.BYBGNPTUT`. Pydantic `EmailStr` validation caused 500 Internal Server Error on any large fetch that included these leads.

#### Fixes
- Backend: `page_size` limit increased `100 → 5000`
- Backend: `EmailStr → str` in `LeadBase` schema to tolerate corrupt discovery data
- Frontend: KanbanBoard `page_size` synced to `5000`

#### Result
API now returns all 480 leads successfully. Kanban populates all 13 stages.

---

## Previous phases

### v0.5.1 — Kimi Integration (2026-04-24)
- AI provider routing: Kimi (`kimi-for-coding`) + sentence-transformers embeddings (384 dims)
- Docker env vars for all AI providers
- Embedding alignment with pgvector

### v0.5.0 — Calendar Integration + Booking System (2026-04-24)
- Booking model, Calendar router (event types, availability, bookings CRUD, cancel, send-link)
- Cal.com webhook handler, CRM integration
- Frontend calendar page, navbar update

### v0.4.0 — Auth System (2026-04-24)
- JWT auth, protected routes, multi-tenancy, login page

### v0.3.0 — Email Outreach + CRM Pipeline + Sequences (2026-04-24)
- 4 Celery tasks, email sequences, drip campaigns

### v0.2.0 — Discovery + Research + Dashboard (2026-04-24)
- 4 discovery sources, semantic search

---

## Known issues / next steps

### Blockers for production
| Item | Status | Notes |
|------|--------|-------|
| Colorado SOS | ✅ Working | Official Open Data API |
| Yelp Fusion | ✅ Working | 500 req/day free tier |
| LinkedIn (SerpApi) | ✅ Working | 100 searches/month free tier |
| Auth system | ✅ Working | JWT + RBAC + protected routes |
| Calendar / Booking | ✅ Working | Cal.com integration, local booking model |
| Kimi AI | ✅ Working | `kimi-for-coding` + sentence-transformers embeddings |
| Celery Worker | ✅ Working | Enrichment, follow-ups, DNC sync, daily reports |
| Docker | ✅ Running | All 6 containers up on PC ROG (10.0.0.240) |
| Google Maps | ⏳ Deferred | Outscraper requires payment (401 placeholder) |
| pytest | ⚠️ Blocked | Python 3.14 incompatible with pydantic-core wheels |
| OpenAI API Key | ❌ Placeholder | Kimi replaces OpenAI for now |
| Resend API Key | ❌ Placeholder | Required for actual email delivery |
| Cal.com API Key | ❌ Placeholder | Required for live calendar sync |

### Frontend gaps identified
1. **Campaign "Create" button** — Dead/non-functional (no `onClick`, no create page)
2. **Calendar "Create Booking"** — Only list + cancel exist; no UI to create bookings
3. **Lead detail TypeScript** — Build passes but audit flagged potential issues

### Next priorities (Fase 3-4)
1. Voice AI integration (Retell / Vapi)
2. Production deployment hardening
3. Analytics dashboard enhancements
4. Fix campaign creation flow
5. Add calendar booking creation UI

---

## Environment

### API Keys configured
- `KIMI_API_KEY`: ✅ Configured (via docker-compose)
- `YELP_API_KEY`: ✅ Configured (free tier)
- `SERPAPI_API_KEY`: ✅ Configured (100 searches/month free)
- `PAPERCLIP_API_KEY`: ✅ Configured
- `OUTSCRAPER_API_KEY`: ❌ Placeholder (401)
- `OPENAI_API_KEY`: ❌ Not configured (Kimi replaces)
- `RESEND_API_KEY`: ❌ Not configured
- `CAL_COM_API_KEY`: ❌ Not configured

### Services status (PC ROG @ 10.0.0.240)
| Service | URL | Status |
|---------|-----|--------|
| Paperclip UI | http://100.88.47.99:3100 | ✅ Online |
| Paperclip API | http://100.88.47.99:3100/api | ✅ Online |
| Eko Backend | http://10.0.0.240:8001 | ✅ Running |
| Eko Frontend | http://10.0.0.240:3001 | ✅ Running |
| PostgreSQL | 10.0.0.240:5433 | ✅ Running (healthy) |
| Redis | 10.0.0.240:6380 | ✅ Running (healthy) |
| Celery Worker | — | ✅ Active (processing enrichment) |
| Celery Beat | — | ✅ Active (scheduling) |

---

## Quick commands

```bash
# SSH to host
ssh enderj@10.0.0.240

# Start / restart Docker infrastructure
cd ~/Eko-AI-Bussinnes-Automation
docker compose up -d --build

# Verify backend health
curl http://10.0.0.240:8001/health

# Watch Celery worker logs
docker compose logs -f celery-worker

# Database counts
docker exec -i eko-db psql -U eko -d eko_ai -c "SELECT status, COUNT(*) FROM leads GROUP BY status;"

# Run tests (inside Docker or after deps installed)
cd backend && pytest tests/ -v
```
