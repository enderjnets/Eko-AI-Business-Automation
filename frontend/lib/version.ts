export const CURRENT_VERSION = "0.7.1";

export interface VersionEntry {
  version: string;
  date: string;
  title: string;
  changes: string[];
}

export const CHANGELOG: VersionEntry[] = [
  {
    version: "0.7.1",
    date: "2026-05-05",
    title: "Inbox, DNS, Voice Agent y UX",
    changes: [
      "Inbox agrupado por lead con conteo de mensajes y threading de conversaciones",
      "Webhook de correos entrantes con auto-respuesta IA y keywords en inglés/español",
      "Formateo de emails: texto plano a HTML con párrafos y saltos de línea",
      "Pixel de tracking para apertura de correos",
      "Configuración DNS completa: SPF + DKIM + DMARC para biz.ekoaiautomation.com",
      "Soporte para Google Meet en reservas de demo (alternativa a Zoom)",
      "Manejo de zona horaria en links de calendario (America/Denver)",
      "Fix de RLS/workspace: migración de interacciones legacy a workspace default",
      "Botón de versión + modal de historial de cambios en navbar",
      "Creación manual de leads desde /leads (formulario modal con validación)",
    ],
  },
  {
    version: "0.7.0",
    date: "2026-04-28",
    title: "FASE 8: AI Proposal Generator + Email Reply Agent + VAPI Voice Agent",
    changes: [
      "AI Proposal Generator: generación automática de propuestas personalizadas",
      "Email Reply Agent: respuestas automáticas inteligentes a emails entrantes",
      "VAPI Voice Agent: agente de voz con integración VAPI para llamadas",
    ],
  },
  {
    version: "0.6.1",
    date: "2026-04-26",
    title: "Pipeline Hardening + Full Sales Cycle Demo",
    changes: [
      "Pipeline fix: valid transitions, interaction tracking, score-0 hardening",
      "Full sales cycle demo features",
    ],
  },
  {
    version: "0.6.0",
    date: "2026-04-25",
    title: "Enrichment Pipeline Hardening",
    changes: [
      "Enrichment pipeline hardening y mejoras de estabilidad",
      "Client-side sort fix + autocomplete + deploy hardening",
    ],
  },
  {
    version: "0.5.0",
    date: "2026-04-24",
    title: "Booking System + Cal.com Integration",
    changes: [
      "Sistema de reservas de citas integrado",
      "Integración con Cal.com para scheduling",
      "Webhooks de calendario y recordatorios",
    ],
  },
  {
    version: "0.4.0",
    date: "2026-04-24",
    title: "JWT Auth + Protected Routes + Multi-tenancy",
    changes: [
      "Sistema de autenticación JWT",
      "Rutas protegidas en frontend",
      "Multi-tenancy con workspaces",
    ],
  },
  {
    version: "0.3.0",
    date: "2026-04-24",
    title: "Email Sequences + Celery + CRM Automation",
    changes: [
      "Secuencias de emails automatizadas",
      "Tareas en background con Celery + Redis",
      "Automatización de CRM",
    ],
  },
  {
    version: "0.2.0",
    date: "2026-04-24",
    title: "Outreach + CRM Pipeline Completo",
    changes: [
      "Pipeline completo de outreach",
      "CRM con gestión de leads y deals",
    ],
  },
  {
    version: "0.1.0",
    date: "2026-04-23",
    title: "MVP Scaffolding — Discovery, Research, Outreach, Dashboard",
    changes: [
      "Discovery: búsqueda de negocios en Google Maps, Yelp, LinkedIn",
      "Research: enriquecimiento de leads con IA",
      "Outreach: envío de emails personalizados",
      "Dashboard: panel de control con métricas",
      "Integración con Paperclip AI",
    ],
  },
];
