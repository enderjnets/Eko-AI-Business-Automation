"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { ArrowRight, ArrowLeft, Send } from "lucide-react";
import { useVirtualizer } from "@tanstack/react-virtual";
import { crmApi, leadsApi } from "@/lib/api";

const PIPELINE_STAGES = [
  { key: "discovered", label: "Descubiertos", color: "bg-gray-500" },
  { key: "enriched", label: "Enriquecidos", color: "bg-blue-500" },
  { key: "scored", label: "Scoring", color: "bg-indigo-500" },
  { key: "contacted", label: "Contactados", color: "bg-yellow-500" },
  { key: "engaged", label: "Engaged", color: "bg-orange-500" },
  { key: "meeting_booked", label: "Citas", color: "bg-purple-500" },
  { key: "proposal_sent", label: "Propuestas", color: "bg-pink-500" },
  { key: "negotiating", label: "Negociando", color: "bg-rose-500" },
  { key: "closed_won", label: "Ganados", color: "bg-eko-green" },
  { key: "closed_lost", label: "Perdidos", color: "bg-red-500" },
  { key: "active", label: "Activos", color: "bg-emerald-500" },
  { key: "at_risk", label: "En Riesgo", color: "bg-amber-500" },
  { key: "churned", label: "Churned", color: "bg-stone-500" },
];

// Valid transitions mirroring backend VALID_TRANSITIONS
const VALID_TRANSITIONS: Record<string, string[]> = {
  discovered: ["enriched", "contacted"],
  enriched: ["scored", "contacted"],
  scored: ["contacted", "closed_lost"],
  contacted: ["engaged", "closed_lost"],
  engaged: ["meeting_booked", "proposal_sent", "closed_lost"],
  meeting_booked: ["proposal_sent", "negotiating", "closed_won", "closed_lost"],
  proposal_sent: ["negotiating", "closed_won", "closed_lost"],
  negotiating: ["closed_won", "closed_lost"],
  closed_won: ["active"],
  closed_lost: ["discovered"],
  active: ["at_risk"],
  at_risk: ["churned", "active"],
  churned: [],
};

interface Lead {
  id: number;
  business_name: string;
  category: string;
  city: string;
  total_score: number;
  status: string;
  email?: string;
  phone?: string;
}

const getScoreColor = (score: number) => {
  if (score >= 70) return "text-eko-green";
  if (score >= 50) return "text-gold";
  if (score >= 30) return "text-orange-400";
  return "text-gray-500";
};

const getValidNextStages = (status: string): string[] => {
  return VALID_TRANSITIONS[status] || [];
};

const getValidPrevStages = (status: string): string[] => {
  const prev: string[] = [];
  for (const [from, toList] of Object.entries(VALID_TRANSITIONS)) {
    if (toList.includes(status)) {
      prev.push(from);
    }
  }
  return prev;
};

interface KanbanColumnProps {
  stage: (typeof PIPELINE_STAGES)[number];
  stageLeads: Lead[];
  onTransition: (lead: Lead, newStatus: string) => void;
  onSendEmail: (lead: Lead) => void;
  actionLoading: Record<number, boolean>;
}

function KanbanColumn({
  stage,
  stageLeads,
  onTransition,
  onSendEmail,
  actionLoading,
}: KanbanColumnProps) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: stageLeads.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 96,
    overscan: 5,
  });

  const virtualItems = virtualizer.getVirtualItems();

  return (
    <div className="w-72 flex-shrink-0 rounded-xl border border-white/5 bg-white/[0.02] flex flex-col max-h-[600px]">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-white/5 flex-shrink-0">
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${stage.color}`} />
          <span className="text-sm font-medium">{stage.label}</span>
        </div>
        <span className="text-xs text-gray-500 bg-white/5 px-2 py-0.5 rounded-full">
          {stageLeads.length}
        </span>
      </div>

      {/* Virtualized Lead List */}
      <div
        ref={parentRef}
        className="p-3 overflow-y-auto flex-1"
        style={{ contain: "strict" }}
      >
        {stageLeads.length === 0 ? (
          <div className="text-center py-8 text-gray-600 text-xs">No leads</div>
        ) : (
          <div
            style={{
              height: `${virtualizer.getTotalSize()}px`,
              width: "100%",
              position: "relative",
            }}
          >
            {virtualItems.map((virtualItem) => {
              const lead = stageLeads[virtualItem.index];
              const validNext = getValidNextStages(lead.status);
              const validPrev = getValidPrevStages(lead.status);
              const isLoading = actionLoading[lead.id];

              return (
                <div
                  key={lead.id}
                  ref={virtualizer.measureElement}
                  data-index={virtualItem.index}
                  style={{
                    position: "absolute",
                    top: 0,
                    left: 0,
                    width: "100%",
                    transform: `translateY(${virtualItem.start}px)`,
                  }}
                  className="px-1 py-1"
                >
                  <div className="rounded-lg border border-white/5 bg-white/[0.03] p-3 hover:bg-white/[0.05] transition-colors">
                    <div className="flex items-start justify-between">
                      <h4 className="font-medium text-sm pr-2">{lead.business_name}</h4>
                      {lead.total_score > 0 ? (
                        <span
                          className={`text-xs font-bold flex-shrink-0 ${getScoreColor(lead.total_score)}`}
                        >
                          {Math.round(lead.total_score)}
                        </span>
                      ) : (
                        <span className="text-xs text-gray-600 flex-shrink-0">—</span>
                      )}
                    </div>
                    <p className="text-xs text-gray-500 mt-0.5">{lead.city}</p>

                    {/* Actions */}
                    <div className="flex items-center gap-1 mt-2 flex-wrap">
                      {/* Backward transitions */}
                      {validPrev.map((prevStatus) => (
                        <button
                          key={prevStatus}
                          onClick={() => onTransition(lead, prevStatus)}
                          disabled={isLoading}
                          className="p-1 rounded hover:bg-white/10 text-gray-500 disabled:opacity-50"
                          title={`Mover a ${PIPELINE_STAGES.find((s) => s.key === prevStatus)?.label}`}
                        >
                          <ArrowLeft className="w-3.5 h-3.5" />
                        </button>
                      ))}

                      {/* Send email */}
                      {lead.email && validNext.length > 0 && (
                        <button
                          onClick={() => onSendEmail(lead)}
                          disabled={isLoading}
                          className="p-1 rounded hover:bg-white/10 text-eko-blue disabled:opacity-50"
                          title="Enviar email"
                        >
                          <Send className="w-3.5 h-3.5" />
                        </button>
                      )}

                      {/* Forward transitions */}
                      {validNext.map((nextStatus) => (
                        <button
                          key={nextStatus}
                          onClick={() => onTransition(lead, nextStatus)}
                          disabled={isLoading}
                          className="p-1 rounded hover:bg-white/10 text-gray-500 disabled:opacity-50"
                          title={`Mover a ${PIPELINE_STAGES.find((s) => s.key === nextStatus)?.label}`}
                        >
                          <ArrowRight className="w-3.5 h-3.5" />
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

export default function KanbanBoard() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<Record<number, boolean>>({});

  useEffect(() => {
    loadLeads();
  }, []);

  const loadLeads = async () => {
    try {
      // Cap at 2000 leads — virtualizer handles rendering, but we keep
      // network payload reasonable. For larger datasets we should move
      // to server-side filtering by status.
      const res = await leadsApi.list({ page_size: 2000 });
      setLeads(res.data.items || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const transitionLead = useCallback(async (lead: Lead, newStatus: string) => {
    setActionLoading((prev) => ({ ...prev, [lead.id]: true }));
    try {
      await crmApi.transition(lead.id, newStatus);
      loadLeads();
    } catch (err: any) {
      console.error("Transition failed:", err);
      alert(err.response?.data?.detail || "Transición no permitida");
    } finally {
      setActionLoading((prev) => ({ ...prev, [lead.id]: false }));
    }
  }, []);

  const sendEmail = useCallback(async (lead: Lead) => {
    setActionLoading((prev) => ({ ...prev, [lead.id]: true }));
    try {
      await crmApi.contact(lead.id, "email", "initial_outreach");
      loadLeads();
    } catch (err) {
      console.error(err);
    } finally {
      setActionLoading((prev) => ({ ...prev, [lead.id]: false }));
    }
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="animate-spin w-8 h-8 border-2 border-eko-blue border-t-transparent rounded-full" />
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <div className="flex gap-4 min-w-max pb-4">
        {PIPELINE_STAGES.map((stage) => {
          const stageLeads = leads.filter((l) => l.status === stage.key);

          return (
            <KanbanColumn
              key={stage.key}
              stage={stage}
              stageLeads={stageLeads}
              onTransition={transitionLead}
              onSendEmail={sendEmail}
              actionLoading={actionLoading}
            />
          );
        })}
      </div>
    </div>
  );
}
