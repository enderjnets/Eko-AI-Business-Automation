"use client";

import { useState } from "react";
import { Tag, X, ChevronRight } from "lucide-react";

const CHANGELOG = [
  {
    version: "0.6.0",
    date: "2026-04-25",
    title: "Enrichment Pipeline Hardening",
    items: [
      "Celery worker fix — SQLAlchemy mapper error resuelto",
      "Commit-per-lead — UI ve progreso en tiempo real",
      "Kimi JSON parsing robusto (brace counting, markdown stripping)",
      "WebsiteFinder bloquea .pdf / .gov / .mil",
      "Yelp pagination — hasta 200 resultados",
      "Discovery deduplication segura con null values",
      "DiscoveryResponse schema + validación",
      "Cal.com auth fix + email unsubscribe URL",
      "Leads pagination (100/página) + barra de progreso",
      "DiscoveryForm con dropdowns city/state/max_results",
      "fetch() nativo para /discover (CORS workaround)",
    ],
  },
  {
    version: "0.5.1",
    date: "2026-04-24",
    title: "AI Provider Routing (Kimi Integration)",
    items: [
      "Kimi como proveedor AI principal (kimi-for-coding)",
      "sentence-transformers embeddings (384 dims)",
      "AI client: fallback a reasoning_content",
      "Embedding alignment con pgvector",
    ],
  },
  {
    version: "0.5.0",
    date: "2026-04-24",
    title: "Calendar Integration + Booking System",
    items: [
      "Booking model con Cal.com sync",
      "Calendar router: event types, availability, bookings CRUD",
      "CRM integration: send booking link",
      "Cal.com webhook handler",
      "Frontend calendar page",
    ],
  },
  {
    version: "0.4.0",
    date: "2026-04-24",
    title: "Auth System: JWT + Protected Routes",
    items: [
      "User model con roles (admin, manager, agent)",
      "JWT security: bcrypt, access/refresh tokens",
      "Auth router: login, register, refresh, dev-login",
      "Protected routes en toda la API",
      "Multi-tenancy por owner_id",
      "Frontend: AuthContext, login page, route guards",
    ],
  },
  {
    version: "0.3.0",
    date: "2026-04-24",
    title: "Email Outreach + CRM Pipeline + Sequences",
    items: [
      "4 Celery scheduled tasks (follow-ups, enrichment, DNC, reports)",
      "Email sequences (drip campaigns)",
      "Sequence models + enrollment",
      "Dry-run mode para testing",
    ],
  },
  {
    version: "0.2.0",
    date: "2026-04-24",
    title: "Discovery + Research + Dashboard",
    items: [
      "4 fuentes de discovery (Yelp, LinkedIn, Colorado SOS, Google Maps)",
      "Semantic search con pgvector + embeddings",
      "Dashboard con stats y pipeline",
    ],
  },
  {
    version: "0.1.0",
    date: "2026-04-07",
    title: "MVP Release",
    items: [
      "FastAPI + async SQLAlchemy + pgvector",
      "Next.js 14 + Tailwind CSS",
      "DiscoveryAgent + ResearchAgent + EmailOutreach",
      "CRM Pipeline con 10 etapas",
      "Paperclip integration",
      "Docker Compose setup",
    ],
  },
];

export default function VersionBadge() {
  const [open, setOpen] = useState(false);
  const [expanded, setExpanded] = useState<string | null>("0.6.0");

  return (
    <>
      {/* Floating Badge */}
      <button
        onClick={() => setOpen(true)}
        className="fixed bottom-6 right-6 z-40 flex items-center gap-2 rounded-full border border-eko-blue/30 bg-eko-graphite/90 px-4 py-2 text-sm font-medium text-eko-blue shadow-lg backdrop-blur-sm transition-all hover:bg-eko-blue/10 hover:scale-105 hover:border-eko-blue/50"
        title="Ver changelog"
      >
        <Tag className="w-3.5 h-3.5" />
        <span>v0.6.0</span>
      </button>

      {/* Modal */}
      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          {/* Backdrop */}
          <div
            className="absolute inset-0 bg-black/60 backdrop-blur-sm"
            onClick={() => setOpen(false)}
          />

          {/* Modal Content */}
          <div className="relative w-full max-w-2xl max-h-[85vh] rounded-2xl border border-gray-700 bg-eko-graphite shadow-2xl flex flex-col">
            {/* Header */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-gray-700">
              <div>
                <h2 className="text-lg font-bold font-display text-eko-white">
                  Changelog
                </h2>
                <p className="text-xs text-gray-400 mt-0.5">
                  Historial de cambios del sistema
                </p>
              </div>
              <button
                onClick={() => setOpen(false)}
                className="rounded-lg p-2 text-gray-400 hover:text-eko-white hover:bg-gray-700/50 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Scrollable Content */}
            <div className="overflow-y-auto px-6 py-4 space-y-3">
              {CHANGELOG.map((entry) => {
                const isExpanded = expanded === entry.version;
                return (
                  <div
                    key={entry.version}
                    className={`rounded-xl border transition-all ${
                      isExpanded
                        ? "border-eko-blue/30 bg-eko-blue/5"
                        : "border-gray-700/50 bg-gray-800/30 hover:border-gray-600"
                    }`}
                  >
                    <button
                      onClick={() =>
                        setExpanded(isExpanded ? null : entry.version)
                      }
                      className="w-full flex items-center justify-between px-4 py-3 text-left"
                    >
                      <div className="flex items-center gap-3">
                        <span className="inline-flex items-center rounded-md bg-eko-blue/10 px-2 py-0.5 text-xs font-semibold text-eko-blue">
                          v{entry.version}
                        </span>
                        <span className="text-sm text-gray-400">
                          {entry.date}
                        </span>
                      </div>
                      <ChevronRight
                        className={`w-4 h-4 text-gray-400 transition-transform ${
                          isExpanded ? "rotate-90" : ""
                        }`}
                      />
                    </button>

                    {isExpanded && (
                      <div className="px-4 pb-4">
                        <h3 className="text-sm font-semibold text-eko-white mb-2">
                          {entry.title}
                        </h3>
                        <ul className="space-y-1.5">
                          {entry.items.map((item, idx) => (
                            <li
                              key={idx}
                              className="flex items-start gap-2 text-sm text-gray-300"
                            >
                              <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-eko-green" />
                              <span>{item}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            {/* Footer */}
            <div className="px-6 py-3 border-t border-gray-700 text-center">
              <span className="text-xs text-gray-500">
                Eko AI Business Automation — versión actual v0.6.0
              </span>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
