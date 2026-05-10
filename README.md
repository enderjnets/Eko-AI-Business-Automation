# Eko AI Business Automation

Sistema de Agentes Autónomos para Prospección, Seguimiento y Ventas — desarrollado por **Eko AI Automation LLC** (Denver, CO).

## Arquitectura

Sistema multi-agente construido con **LangGraph** que orquesta todo el ciclo de ventas:

| Agente | Función |
|--------|---------|
| **Discovery** | Prospección geolocalizada (Google Maps, LinkedIn, Yelp, SOS CO) |
| **Research** | Enriquecimiento de leads con NLP y análisis de brechas |
| **Outreach** | Contacto multicanal: email, voz, SMS |
| **CRM** | Pipeline, lead scoring dinámico, seguimiento adaptativo |
| **Customer Success** | Onboarding, monitoreo de salud, prevención de churn |
| **Compliance** | Validación TCPA, CAN-SPAM, CPA Colorado, FCC AI Rule |

## Stack Tecnológico

- **Backend**: Python 3.11, FastAPI, LangGraph, SQLAlchemy, Celery
- **Frontend**: Next.js 14, Tailwind CSS, TanStack Query
- **Database**: PostgreSQL 15 + pgvector
- **Cache/Queue**: Redis
- **LLM**: OpenAI GPT-4o
- **Email**: Resend
- **Voice**: Retell AI / Vapi AI
- **Scraping**: Outscraper, Apify
- **Calendar**: Cal.com

## Quick Start

### Requisitos

- Docker & Docker Compose
- Node.js 20+ (para desarrollo frontend local)
- API keys: OpenAI, Resend, Outscraper

### 1. Clonar y configurar

```bash
git clone https://github.com/enderjnets/Eko-AI-Business-Automation.git
cd Eko-AI-Business-Automation
cp .env.example .env
# Editar .env con tus API keys
```

### 2. Levantar servicios

```bash
docker-compose up -d
```

Esto inicia:
- PostgreSQL en `localhost:5432`
- Redis en `localhost:6379`
- Backend API en `http://localhost:8000`
- Frontend en `http://localhost:3000`

### 3. Verificar

```bash
curl http://localhost:8000/health
```

### 4. Acceder al dashboard

Abre `http://localhost:3000` en tu navegador.

## API Endpoints

### Leads
- `GET /api/v1/leads` — Listar leads
- `POST /api/v1/leads` — Crear lead manual
- `GET /api/v1/leads/{id}` — Obtener lead
- `PATCH /api/v1/leads/{id}` — Actualizar lead
- `POST /api/v1/leads/{id}/enrich` — Enriquecer con ResearchAgent
- `POST /api/v1/leads/discover` — Ejecutar DiscoveryAgent

### Campañas
- `GET /api/v1/campaigns` — Listar campañas
- `POST /api/v1/campaigns` — Crear campaña
- `POST /api/v1/campaigns/{id}/launch` — Lanzar campaña
- `POST /api/v1/campaigns/{id}/pause` — Pausar campaña

### Emails
- `POST /api/v1/emails/{lead_id}/send` — Enviar email
- `POST /api/v1/emails/{lead_id}/generate-and-send` — Generar y enviar con AI

### Analytics
- `GET /api/v1/analytics/pipeline` — Resumen del pipeline
- `GET /api/v1/analytics/performance` — Métricas de rendimiento

## Estructura del Proyecto

```
├── backend/
│   ├── app/
│   │   ├── agents/           # LangGraph agents
│   │   ├── api/v1/           # FastAPI routers
│   │   ├── db/               # SQLAlchemy models & migrations
│   │   ├── models/           # Database models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # External API integrations
│   │   └── tasks/            # Celery background tasks
│   └── tests/
├── frontend/
│   ├── app/                  # Next.js App Router
│   ├── components/           # React components
│   └── lib/                  # API client & utilities
├── docker-compose.yml
└── docs/
```

## Fases de Desarrollo (MVP Rápido)

| Fase | Semana | Entregable |
|------|--------|-----------|
| 1 | 1-2 | Discovery + Research + Dashboard |
| 2 | 3-4 | Email Outreach + CRM Pipeline |
| 3 | 5-6 | Voice AI + Calendar integration |
| 4 | 7-8 | Customer Success + Analytics |
| 5 | 9-10 | Compliance + Production deploy |

## Cumplimiento Normativo

- **TCPA**: Registro de consentimientos, validación previa a contacto
- **CAN-SPAM**: Unsubscribe funcional en todos los emails
- **CPA Colorado**: Derecho de acceso, borrado y opt-out
- **FCC AI Rule**: Divulgación de IA en llamadas y emails

## Licencia

Proprietary — Eko AI Automation LLC

---

**Contacto**: eko@ekoai.com | Denver, CO
