import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from app.services.tenant_context import resolve_tenant, set_workspace_id

from app.config import get_settings
# Sentry observability (optional — only loads if SENTRY_DSN is set)
try:
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    from sentry_sdk.integrations.starlette import StarletteIntegration
    settings = get_settings()
    if settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            integrations=[
                StarletteIntegration(),
                FastApiIntegration(),
            ],
            traces_sample_rate=1.0 if settings.is_development else 0.2,
        )
        logging.info("[Sentry] Observability initialized")
except Exception:
    pass

from app.api.v1 import leads, campaigns, emails, analytics, webhooks, crm, sequences, auth, calendar, phone_calls, settings as settings_router, deals, proposals, voice_agent, checkout, webhooks_stripe, metadata_objects, metadata_fields, views, dynamic_data, workspaces

# Ensure all models are registered in Base.metadata
from app.models.lead import Lead  # noqa: F401
from app.models.sequence import EmailSequence, SequenceStep, SequenceEnrollment  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.booking import Booking  # noqa: F401
from app.models.phone_call import PhoneCall  # noqa: F401
from app.models.setting import AppSetting  # noqa: F401
from app.models.deal import Deal  # noqa: F401
from app.models.proposal import Proposal  # noqa: F401
from app.models.payment import Payment  # noqa: F401
from app.models.object_metadata import ObjectMetadata  # noqa: F401
from app.models.field_metadata import FieldMetadata  # noqa: F401
from app.models.dynamic_record import DynamicRecord  # noqa: F401
from app.models.view import View, ViewField, ViewFilter, ViewSort  # noqa: F401
from app.models.workspace import Workspace, WorkspaceMember  # noqa: F401
from app.db.base import init_db

settings = get_settings()

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Eko AI Business Automation...")
    await init_db()
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Sistema de Agentes Autónomos para Prospección, Seguimiento y Ventas",
    lifespan=lifespan,
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
)

# Tenant resolution middleware — stores workspace_id in request.state
@app.middleware("http")
async def tenant_middleware(request: Request, call_next):
    from app.services.tenant_context import resolve_tenant, set_workspace_id
    from app.db.base import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        try:
            tenant = await resolve_tenant(request, db=db)
            request.state.workspace_id = tenant.workspace_id
            request.state.tenant_user = tenant.user
            set_workspace_id(tenant.workspace_id)
        except Exception:
            request.state.workspace_id = None
            request.state.tenant_user = None
            set_workspace_id(None)
    response = await call_next(request)
    return response

# CORS
_cors_origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (audio notes, etc.)
app.mount("/audio", StaticFiles(directory="/app/static/audio"), name="audio")

# API Routes v1
app.include_router(leads.router, prefix="/api/v1/leads", tags=["leads"])
app.include_router(campaigns.router, prefix="/api/v1/campaigns", tags=["campaigns"])
app.include_router(emails.router, prefix="/api/v1/emails", tags=["emails"])
app.include_router(crm.router, prefix="/api/v1/crm", tags=["crm"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(sequences.router, prefix="/api/v1/sequences", tags=["sequences"])
app.include_router(calendar.router, prefix="/api/v1/calendar", tags=["calendar"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(phone_calls.router, prefix="/api/v1/phone-calls", tags=["phone_calls"])
app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["webhooks"])
app.include_router(settings_router.router, prefix="/api/v1/settings", tags=["settings"])
app.include_router(deals.router, prefix="/api/v1/deals", tags=["deals"])
app.include_router(proposals.router, prefix="/api/v1/proposals", tags=["proposals"])
app.include_router(voice_agent.router, prefix="/api/v1/voice-agent", tags=["voice_agent"])
app.include_router(checkout.router, prefix="/api/v1/checkout", tags=["checkout"])
app.include_router(webhooks_stripe.router, prefix="/api/v1/webhooks", tags=["webhooks"])

# Workspace routes
app.include_router(workspaces.router, prefix="/api/v1/workspaces", tags=["workspaces"])

# Metadata engine routes
app.include_router(metadata_objects.router, prefix="/api/v1/metadata/objects", tags=["metadata-objects"])
app.include_router(metadata_fields.router, prefix="/api/v1/metadata/fields", tags=["metadata-fields"])
app.include_router(views.router, prefix="/api/v1/views", tags=["views"])
app.include_router(dynamic_data.router, prefix="/api/v1/data", tags=["dynamic-data"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": settings.APP_VERSION, "env": settings.ENVIRONMENT}


@app.get("/")
async def root():
    return {
        "message": "Eko AI Business Automation API",
        "docs": "/docs",
        "version": settings.APP_VERSION,
    }


BOOK_DEMO_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Book a Demo — Eko AI</title>
<style>
:root { --bg:#0B1120; --card:#111827; --text:#F3F4F6; --muted:#9CA3AF; --blue:#3B82F6; --blue-d:#2563EB; }
* { box-sizing:border-box; }
body { margin:0; font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif; background:var(--bg); color:var(--text); display:flex; align-items:center; justify-content:center; min-height:100vh; padding:24px; }
.card { background:var(--card); border:1px solid rgba(255,255,255,0.06); border-radius:16px; padding:32px; width:100%; max-width:480px; }
h1 { margin:0 0 6px; font-size:24px; }
p.sub { margin:0 0 24px; color:var(--muted); font-size:14px; }
label { display:block; font-size:13px; color:var(--muted); margin-bottom:6px; }
input, textarea, select {
  width:100%; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.08);
  border-radius:10px; padding:12px 14px; color:var(--text); font-size:14px;
}
input:focus, textarea:focus, select:focus { outline:none; border-color:var(--blue); }
::placeholder { color:#6B7280; }
.field { margin-bottom:16px; }
.times { display:grid; grid-template-columns:repeat(4,1fr); gap:8px; }
.time-btn {
  background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.08);
  border-radius:8px; padding:8px 0; color:var(--text); font-size:13px; cursor:pointer;
}
.time-btn:hover { border-color:rgba(255,255,255,0.2); }
.time-btn.active { background:var(--blue); border-color:var(--blue); }
button[type=submit] {
  width:100%; background:var(--blue); color:#fff; border:none; border-radius:10px;
  padding:14px; font-size:15px; font-weight:600; cursor:pointer; margin-top:8px;
}
button[type=submit]:hover { background:var(--blue-d); }
button[type=submit]:disabled { opacity:0.5; cursor:not-allowed; }
.success { text-align:center; }
.success h2 { margin:0 0 8px; }
.success p { color:var(--muted); margin:0 0 20px; }
.footer { text-align:center; color:#6B7280; font-size:12px; margin-top:20px; }
</style>
</head>
<body>
<div class="card" id="card">
  <h1>Book a Demo</h1>
  <p class="sub">15 minutes to see how Eko AI transforms your business</p>
  <form id="form">
    <div class="field">
      <label>Business name</label>
      <input type="text" id="name" placeholder="e.g. The Pampering Place" required>
    </div>
    <div class="field">
      <label>Email</label>
      <input type="email" id="email" placeholder="you@email.com" required>
    </div>
    <div class="field">
      <label>Preferred date</label>
      <input type="date" id="date" required>
    </div>
    <div class="field">
      <label>Preferred time (MT)</label>
      <div class="times" id="times"></div>
      <input type="hidden" id="time" required>
    </div>
    <div class="field">
      <label>Message (optional)</label>
      <textarea id="message" rows="3" placeholder="Is there something specific you\'d like to see?"></textarea>
    </div>
    <button type="submit" id="submit">Book Demo</button>
  </form>
  <p class="footer">Eko AI — Denver, CO — contact@biz.ekoaiautomation.com</p>
</div>
<script>
const params = new URLSearchParams(location.search);
const prefillEmail = params.get("email") || "";
const prefillName = params.get("name") || "";
if(prefillEmail) document.getElementById("email").value = prefillEmail;
if(prefillName) document.getElementById("name").value = prefillName;

document.getElementById("date").min = new Date().toISOString().split("T")[0];

const slots = ["09:00","09:30","10:00","10:30","11:00","11:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30"];
const timesWrap = document.getElementById("times");
const timeInput = document.getElementById("time");
slots.forEach(t=>{
  const b=document.createElement("button"); b.type="button"; b.className="time-btn"; b.textContent=t;
  b.onclick=()=>{ timesWrap.querySelectorAll(".time-btn").forEach(x=>x.classList.remove("active")); b.classList.add("active"); timeInput.value=t; };
  timesWrap.appendChild(b);
});

document.getElementById("form").addEventListener("submit", async e=>{
  e.preventDefault();
  const btn=document.getElementById("submit"); btn.disabled=true; btn.textContent="Scheduling...";
  const body={
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    date: document.getElementById("date").value,
    time: document.getElementById("time").value,
    message: document.getElementById("message").value,
  };
  try{
    const r=await fetch("/api/v1/calendar/book-demo",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    if(!r.ok) throw new Error("Failed");
    document.getElementById("card").innerHTML=\`<div class="success"><h2>✅ Demo Scheduled!</h2><p>Thank you \${body.name}. We\'ll contact you soon to confirm your demo on \${body.date} at \${body.time} (MT).</p><a href="/" style="color:#3B82F6">Back to home</a></div>\`;
  }catch(err){
    btn.disabled=false; btn.textContent="Book Demo"; alert("Something went wrong. Please try again.");
  }
});
</script>
</body>
</html>'''

@app.get("/book-demo", response_class=HTMLResponse)
async def book_demo_page(request: Request):
    return BOOK_DEMO_HTML
