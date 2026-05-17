

## [0.7.5] — 2026-05-17

### Content Studio Pipeline — Video Fixes + Login Repair + Buffer Caching

#### Pipeline / Content Studio
- **Multi-scene scripts**: `content_creator.py` now generates 4 VIDEO_PROMPTs for shorts and 6 for longs (was 1 and 3)
- **ASS Subtitles**: Replaced SRT with ASS format — DejaVu Sans 28px, bottom-centered, black semi-transparent background box
- **Crossfade Transitions**: Added `crossfade_clips()` using ffmpeg `xfade` filter with 0.8s fade between clips. Fallback to concat demuxer if xfade fails
- **End Frame CTA**: Added `create_end_frame()` using ffmpeg `drawtext` with business name, address, special offer, and price. Duration dynamically calculated to fill remaining audio time
- **Edge-TTS Fallback**: Added `edge-tts>=6.1.0` to requirements.txt. ElevenLabs returns 401, MiniMax TTS returns no audio — Edge-TTS (`es-MX-JorgeNeural`) successfully generates Spanish audio
- **Test Production**: Produced and uploaded short (29.9s, 8.0MB) and long (79.0s, 22.2MB) videos with FLUX + Ken Burns

#### Frontend Fixes
- **Login Repair**: Frontend container moved from default `bridge` network to `eko-ai-bussinnes-automation_default` Docker network so it can resolve `eko-backend`
- **Buffer API Caching**: Added 30-second in-memory cache to `/content-api/posts`, `/content-api/buffer-posts`, `/content-api/limits` routes to avoid Buffer rate limiting
- **Container Mounts**: Added `output/` and `config/` volume mounts to frontend container for local API endpoints (`/pipelines`, `/stats`)
- **TypeScript Fix**: Fixed `for...of` iteration over `Map.keys()` by using `Array.from()` in `api-cache.ts`

#### Auto-publisher
- **Dynamic Video Discovery**: Auto-publisher script now reads actual pipeline JSON outputs instead of hardcoded video URLs
- Detects connected Buffer channels automatically
- Publishes to correct platforms based on video tags

---
# Changelog

## [0.6.1] — 2026-04-29

### Full Sales Cycle Demo — X3nails & Spa / Margie

#### Voice & Inbound
- **VAPI inbound assistant** (`vapi_client.py`) — Created "Eva" assistant with Rachel voice, Claude Sonnet, Deepgram nova-2 transcriber, `book_demo` function tool, bound to `+1-256-364-1727`
- **VAPI webhooks** (`webhooks.py`) — `tool-calls` creates Booking + notifies Ender; `end-of-call-report` logs call data + sends rich summary email + Telegram alert
- **Outbound calls** (`voice_agent.py`) — `POST /voice-agent/calls` with custom assistant, first message auto-generation

#### Email & Auto-Reply
- **Demo invite template** (`templates/emails/demo_invite.py`) — Professional HTML with VAPI phone CTA + booking link CTA
- **Ender notification template** (`templates/emails/ender_notification.py`) — Rich HTML with lead snapshot, pain points, transcript, recording link, calendar link
- **Auto-reply AI** (`email_reply_agent.py`) — Generates contextual English replies with both phone number (`+1-256-364-1727`) and `/book-demo` link CTAs
- **Svix webhook fix** (`webhooks.py`) — Replaced custom signature verification with `standardwebhooks` library; fixed signed content format (`id.timestamp.body`)
- **Resend inbound processing** (`webhooks.py`) — Full inbound email webhook with AI intent analysis, auto-reply, status transitions

#### Booking & Calendar
- **Public booking page** (`main.py`) — `/book-demo` serves inline HTML form with date picker, time slots (9:00–16:30 MT), prefills via query params
- **Calendar links** (`utils/calendar_links.py`) — Google Calendar `.ics` generator for "Add to Calendar" buttons
- **Booking endpoint fix** (`calendar.py`) — Added missing `Interaction` import for `/book-demo` POST

#### Notifications
- **Eko Rog Telegram notifier** (`services/eko_rog_notifier.py`) — Sends booking/call alerts to `@EkoBit_Rog_bot`
- **Sales brief generator** (`services/sales_brief_generator.py`) — AI-generated sales brief on booking creation

#### Infrastructure
- **Docker Compose** — Added `APP_URL`, `FRONTEND_URL`, `ENVIRONMENT`, `CORS_ORIGINS`, `VAPI_*`, `TELEGRAM_*`, `AUTO_REPLY_ENABLED` env vars to all services
- **Config** (`config.py`) — Added `AUTO_REPLY_ENABLED`, VAPI IDs, Telegram config, notification email
- **Frontend build** — `NEXT_PUBLIC_API_URL` set to `https://ender-rog.tail25dc73.ts.net`

---

## [0.6.0] — 2026-04-25

### Enrichment Pipeline Hardening

#### Backend
- **Celery worker fix** — Resolved `InvalidRequestError` by creating `app/models/__init__.py` and importing all models in `celery_app.py` before app initialization
- **Commit-per-lead enrichment** — Both scheduled `enrich_pending_leads` (every 30 min) and manual `enrich-all` endpoint now commit after each individual lead, enabling real-time UI progress tracking
- **Kimi JSON parsing** — Replaced fragile greedy regex with robust `_extract_json()` in `ResearchAgent`:
  - Fast path: direct `json.loads()` for clean responses
  - Markdown stripping: unwraps ` ```json ... ``` ` code blocks
  - Brace counting with string/escape awareness: finds balanced `{}` pairs while respecting JSON string literals
  - Eliminates fallback 50/50 scores from truncated or malformed JSON
- **WebsiteFinder hardening** (`app/agents/research/analyzers/website.py`):
  - Blocks URLs ending in `.pdf`, containing `.gov/`, or `.mil/` to avoid wasting enrichment cycles on government/military documents
  - Prevents CO SOS delinquent records from triggering irrelevant `.gov` PDF scrapes
- **Yelp Fusion pagination** — Added offset pagination so requesting >50 results (up to 200) correctly chains multiple API calls (50 per call) instead of silently capping
- **Discovery deduplication** — Fixed `AttributeError: 'NoneType' object has no attribute 'lower'` when LinkedIn or Colorado SOS return leads with null `city` or `business_name`
- **DiscoveryResponse schema** (`app/schemas/lead.py`) — New `DiscoveryResponse` with `total_found`, `new_leads`, `duplicates_skipped`, `items`. Updated `POST /discover` endpoint to return this instead of `LeadListResponse`, fixing 500 validation errors
- **Cal.com auth fix** (`app/services/cal_com.py`) — Switched from Bearer header to query param (`?apiKey=`) for Cal.com API compatibility
- **Email unsubscribe URL** (`app/agents/outreach/channels/email.py`) — Fixed hardcoded `localhost` unsubscribe link
- **AI client hardening** (`app/utils/ai_client.py`) — Added explicit "Your response must be ONLY valid JSON" instruction to Kimi prompts when `json_mode=True`
- **Docker Compose** — Added `KIMI_API_KEY`, `KIMI_BASE_URL`, `KIMI_MODEL`, `KIMI_EMBEDDING_MODEL`, `OPENAI_BASE_URL`, `OPENAI_MODEL`, `OPENAI_EMBEDDING_MODEL`, `CAL_COM_API_KEY` to all services

#### Frontend
- **Leads pagination** (`frontend/app/leads/page.tsx`) — Added page state with Previous/Next buttons, 100 leads per page
- **Enrichment progress bar** — Real-time progress indicator with polling every 10s, showing processed count, pending count, and percentage
- **DiscoveryForm dropdowns** (`frontend/components/DiscoveryForm.tsx`) — Converted city, state, and max_results to `<select>` menus:
  - 30 Colorado cities pre-populated
  - All 50 US states + DC
  - max_results options: 10, 25, 50, 100, 200
- **Discovery fetch workaround** — Replaced axios with native `fetch()` for `/discover` POST to avoid axios preflight CORS "Network Error" when selecting multiple sources
- **API URL consistency** — Replaced hardcoded `http://10.0.0.240:8001` fetch calls in `leads/page.tsx` with relative `/api/v1/...` paths (Next.js rewrites)

#### Infrastructure / DevEx
- **Frontend Dockerfile** — `NEXT_PUBLIC_API_URL` set to `http://10.0.0.240:8001`
- **Backend config** — `KIMI_BASE_URL` default updated to `https://api.kimi.com/coding/v1`, `KIMI_MODEL` default to `kimi-for-coding`
- **Lead model** — Added missing fields: `review_summary`, `trigger_events`, `pain_points`, `scoring_reason`, `proposal_suggestion`

---

## [0.6.2] — 2026-04-25

### Pipeline Fix — Complete Visibility + Valid Transitions + Interaction Tracking

#### Backend
- **Score 0 validity** (`app/tasks/scheduled.py`, `app/api/v1/leads.py`) — Changed `if lead.urgency_score and lead.fit_score:` to `is not None` checks in 3 places. Defunct businesses with 0/0 scores now correctly transition to `SCORED` instead of getting stuck in `ENRICHED`
- **PATCH transition validation** (`app/api/v1/leads.py`) — `update_lead` endpoint now validates status changes against `VALID_TRANSITIONS` from CRM router. Prevents jumping `discovered` → `closed_won`. Also records an `Interaction` with transition metadata
- **Rate limiter fix** (`app/api/v1/crm.py`) — `_check_contact_rate_limit` now filters `direction="outbound"` so inbound email clicks/opens don't falsely count against the daily limit
- **CRM email interactions** (`app/api/v1/crm.py`) — `contact_lead` now creates an `Interaction` record with channel, template, AI-generated flag, and message_id before committing

#### Frontend
- **KanbanBoard: 13 complete stages** (`frontend/components/KanbanBoard.tsx`) — Added missing `active`, `at_risk`, `churned` stages. Customer lifecycle leads no longer disappear from the pipeline
- **Valid transition arrows** — Replaced broken index-based movement with explicit valid-transition buttons. Backward/forward arrows only appear for transitions allowed by the backend state machine
- **Load all leads** — `page_size: 9999` ensures the Kanban shows every lead regardless of total count
- **User feedback on errors** — Invalid transitions now show an `alert()` with the backend message instead of failing silently in console

#### Pipeline Empty Kanban Fix (v0.6.1-hotfix)
- **page_size limit** (`app/api/v1/leads.py`) — Increased from 100 to 5000. KanbanBoard requesting 9999 caused 422 validation error, leaving pipeline completely empty.
- **Email validation** (`app/schemas/lead.py`) — Changed `EmailStr` to `str` in `LeadBase`. Discovery sources (CO SOS, Yelp) produced corrupt emails like `K@48G9-.BYBGNPTUT` that caused Pydantic `ValidationError` and 500 errors on large fetches.
- **KanbanBoard sync** (`frontend/components/KanbanBoard.tsx`) — `page_size` adjusted from 9999 to 5000 to match backend limit.

---

## [0.5.1] — 2026-04-24

### Fixed: AI Provider Routing (Kimi Integration)

#### Backend
- **Docker Compose env vars**: Added `AI_PROVIDER`, `KIMI_API_KEY`, `KIMI_BASE_URL`, `KIMI_MODEL`, `KIMI_EMBEDDING_MODEL`, `OPENAI_BASE_URL`, `OPENAI_MODEL`, `OPENAI_EMBEDDING_MODEL`, `CAL_COM_API_KEY` to `backend`, `celery-worker`, and `celery-beat` services.
- **Config defaults** (`app/config.py`): Changed `KIMI_BASE_URL` default from Moonshot (`https://api.moonshot.cn/v1`) to Kimi Code API (`https://api.kimi.com/coding/v1`); changed `KIMI_MODEL` default to `kimi-for-coding`.
- **AI client** (`app/utils/ai_client.py`):
  - Added fallback to `reasoning_content` when `content` is empty (required for `kimi-for-coding` model).
  - Fixed `TypeError` in `generate_embedding`: `SentenceTransformer.encode()` does not accept `convert_to_list`; now uses `.tolist()`.
- **Embeddings alignment**: `sentence-transformers` (`all-MiniLM-L6-v2`) generates 384-dim embeddings, matching `Lead.Vector(384)` in the database schema.

---

## [0.5.0] — 2026-04-24

### Calendar Integration + Booking System

#### Backend
- **Booking model** (`app/models/booking.py`) — tracks meetings locally with Cal.com sync
- **Calendar router** (`app/api/v1/calendar.py`):
  - `GET /calendar/event-types` — List Cal.com event types
  - `POST /calendar/availability` — Get available time slots
  - `GET /calendar/bookings` — List bookings with filters (upcoming, by lead, by status)
  - `POST /calendar/bookings` — Create booking for a lead (syncs with Cal.com if configured)
  - `POST /calendar/bookings/{id}/cancel` — Cancel booking locally and on Cal.com
  - `POST /calendar/send-link` — Send booking link via email to a lead
- **CRM integration**: `POST /crm/{lead_id}/send-booking-link` — Send booking link directly from pipeline
- **Webhook handler** (`/webhooks/calcom`) already existed — auto-updates lead to `MEETING_BOOKED` on Cal.com booking

#### Frontend
- **Calendar page** (`frontend/app/calendar/page.tsx`) — View upcoming/all/past meetings, cancel bookings, join video links
- **Navbar** updated with Calendar navigation link
- **API client** updated with `calendarApi` methods

#### Tests
- `tests/test_calendar.py` — Booking model enums, calendar API endpoints, schemas

---

## [0.4.0] — 2026-04-24

### Auth System: JWT + Protected Routes + Multi-tenancy

#### Backend
- **User model** (`app/models/user.py`) with roles: `admin`, `manager`, `agent`
- **JWT security** (`app/core/security.py`): password hashing (bcrypt), access/refresh tokens, `get_current_user` dependency, role-based guards (`get_current_admin`)
- **Auth router** (`app/api/v1/auth.py`):
  - `POST /auth/login` — JWT token pair
  - `POST /auth/register` — Admin-only user creation
  - `POST /auth/refresh` — Token refresh
  - `GET /auth/me` — Current user profile
  - `PATCH /auth/me` — Update profile
  - `GET /auth/users` — List users (admin)
  - `POST /auth/dev-login` — Development bypass (creates admin dev user)
- **Protected routes**: All existing API endpoints now require Bearer token (`leads`, `campaigns`, `crm`, `sequences`, `emails`, `analytics`)
- **Multi-tenancy**: Non-admin users only see leads they own or are assigned to; `owner_id` auto-assigned on lead creation/discovery

#### Frontend
- **Auth context** (`frontend/contexts/AuthContext.tsx`): login state, auto-redirect, token persistence in localStorage
- **Login page** (`frontend/app/login/page.tsx`): email/password form + dev login button
- **API client** (`frontend/lib/api.ts`): Axios interceptors inject Bearer token; auto-redirect to `/login` on 401
- **Navbar** updated: displays current user name/role + logout button
- **Route protection**: Unauthenticated users redirected to `/login`

#### Tests
- `tests/test_auth.py` — Password hashing, JWT encode/decode, token expiration, role-based access control, router endpoints

---

## [0.3.0] — 2026-04-24

### Fase 2 Complete: Email Outreach + CRM Pipeline + Sequences

#### Celery Scheduled Tasks (Implemented)
- **`process_follow_ups`** — Hourly task: finds leads with `next_follow_up_at <= now`, sends AI-generated follow-up emails, records interactions, respects rate limits and cooldowns
- **`enrich_pending_leads`** — Every 30 min: auto-enriches `DISCOVERED` leads via `ResearchAgent`, auto-scores and transitions to `ENRICHED`/`SCORED`
- **`sync_dnc_registry`** — Monthly: marks leads with 3+ bounces as `do_not_contact`, archives opt-outs older than 2 years (CPA Colorado compliance)
- **`generate_daily_report`** — Daily at 8am MT: pipeline summary, new leads, emails sent, conversion rate; logged to Paperclip

#### Email Sequences (Drip Campaigns)
- New models: `EmailSequence`, `SequenceStep`, `SequenceEnrollment`
- New API: `GET/POST/PATCH /api/v1/sequences`, steps CRUD, enroll leads, execute sequences
- Sequence step types: `email`, `wait`, `condition`, `sms`, `call`
- Dry-run mode for testing sequences before live execution
- Auto-advances enrolled leads through steps with configurable delays

#### Infrastructure
- Added `celery-beat` service to `docker-compose.yml` with scheduled tasks
- `celery_app.py` now includes `beat_schedule` with all 4 tasks
- Added missing env vars to docker-compose: `YELP_API_KEY`, `SERPAPI_API_KEY`, `PAPERCLIP_API_KEY`, `CORS_ORIGINS`

#### Tests
- `tests/test_scheduled.py` — Celery task wrappers and async helpers
- `tests/test_sequences.py` — Sequence schemas, models, and API logic

---

## [0.2.0] — 2026-04-24

### Fase 1 Complete: Discovery + Research + Dashboard

#### Discovery Sources
- **Yelp** — Web scraping source with BeautifulSoup + httpx
- **LinkedIn** — Apify actor integration (`harvestapi/linkedin-company`)
- **Colorado SOS** — Official Colorado Open Data API (Socrata) + Apify fallback
- Multi-source selection UI in DiscoveryForm (Google Maps, Yelp, LinkedIn, Colorado SOS)

#### Semantic Search
- New `POST /api/v1/leads/search` endpoint using pgvector + OpenAI embeddings
- Automatic embedding generation on lead creation and enrichment
- Semantic search toggle in Leads page frontend

#### UX Improvements
- Removed `window.location.reload()` anti-pattern from dashboard
- Added reactive `refreshTrigger` to RecentLeads component
- CORS origins now configurable via `CORS_ORIGINS` env var

#### Tests
- `tests/test_discovery.py` — Google Maps, Yelp, LinkedIn, Colorado SOS sources
- `tests/test_research.py` — ResearchAgent enrichment pipeline

#### Infrastructure
- Added `beautifulsoup4` to requirements
- Added `ApifyClient` service for actor orchestration
- Added `update_lead_embedding` utility for vector search

---

## [0.1.0] — 2026-04-07

### MVP Release
- FastAPI backend with async SQLAlchemy + pgvector
- Next.js 14 frontend with Tailwind CSS
- DiscoveryAgent (Google Maps via Outscraper)
- ResearchAgent (Website analysis + GPT-4o scoring)
- EmailOutreach (Resend + AI-generated templates)
- CRM Pipeline with 10 stages
- Paperclip integration for agent traceability
- Docker Compose setup (PostgreSQL, Redis, backend, frontend, Celery)
