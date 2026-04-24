"use client";

import { useState, useEffect } from "react";
import { ArrowRight, ArrowLeft, Mail, Phone, Calendar, Send } from "lucide-react";
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
];

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

export default function KanbanBoard() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedLead, setSelectedLead] = useState<Lead | null>(null);
  const [actionLoading, setActionLoading] = useState(false);

  useEffect(() => {
    loadLeads();
  }, []);

  const loadLeads = async () => {
    try {
      const res = await leadsApi.list({ page_size: 100 });
      setLeads(res.data.items || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const moveLead = async (lead: Lead, direction: "forward" | "backward") => {
    const currentIndex = PIPELINE_STAGES.findIndex((s) => s.key === lead.status);
    const newIndex = direction === "forward" ? currentIndex + 1 : currentIndex - 1;
    
    if (newIndex < 0 || newIndex >= PIPELINE_STAGES.length) return;
    
    const newStatus = PIPELINE_STAGES[newIndex].key;
    setActionLoading(true);
    
    try {
      await crmApi.transition(lead.id, newStatus);
      loadLeads();
    } catch (err) {
      console.error(err);
    } finally {
      setActionLoading(false);
    }
  };

  const sendEmail = async (lead: Lead) => {
    setActionLoading(true);
    try {
      await crmApi.contact(lead.id, "email", "initial_outreach");
      loadLeads();
    } catch (err) {
      console.error(err);
    } finally {
      setActionLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 70) return "text-eko-green";
    if (score >= 50) return "text-gold";
    if (score >= 30) return "text-orange-400";
    return "text-gray-500";
  };

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
            <div
              key={stage.key}
              className="w-72 flex-shrink-0 rounded-xl border border-white/5 bg-white/[0.02]"
            >
              {/* Header */}
              <div className="flex items-center justify-between px-4 py-3 border-b border-white/5">
                <div className="flex items-center gap-2">
                  <div className={`w-2 h-2 rounded-full ${stage.color}`} />
                  <span className="text-sm font-medium">{stage.label}</span>
                </div>
                <span className="text-xs text-gray-500 bg-white/5 px-2 py-0.5 rounded-full">
                  {stageLeads.length}
                </span>
              </div>
              
              {/* Leads */}
              <div className="p-3 space-y-2 max-h-[600px] overflow-y-auto">
                {stageLeads.map((lead) => (
                  <div
                    key={lead.id}
                    className="rounded-lg border border-white/5 bg-white/[0.03] p-3 hover:bg-white/[0.05] transition-colors cursor-pointer"
                    onClick={() => setSelectedLead(lead)}
                  >
                    <div className="flex items-start justify-between">
                      <h4 className="font-medium text-sm">{lead.business_name}</h4>
                      {lead.total_score > 0 && (
                        <span className={`text-xs font-bold ${getScoreColor(lead.total_score)}`}>
                          {Math.round(lead.total_score)}
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-gray-500 mt-0.5">{lead.city}</p>
                    
                    {/* Actions */}
                    <div className="flex items-center gap-1 mt-2">
                      {stage.key !== "discovered" && (
                        <button
                          onClick={(e) => { e.stopPropagation(); moveLead(lead, "backward"); }}
                          disabled={actionLoading}
                          className="p-1 rounded hover:bg-white/10 text-gray-500 disabled:opacity-50"
                        >
                          <ArrowLeft className="w-3.5 h-3.5" />
                        </button>
                      )}
                      
                      {lead.email && stage.key !== "closed_won" && stage.key !== "closed_lost" && (
                        <button
                          onClick={(e) => { e.stopPropagation(); sendEmail(lead); }}
                          disabled={actionLoading}
                          className="p-1 rounded hover:bg-white/10 text-eko-blue disabled:opacity-50"
                          title="Send email"
                        >
                          <Send className="w-3.5 h-3.5" />
                        </button>
                      )}
                      
                      {stage.key !== "closed_won" && stage.key !== "closed_lost" && (
                        <button
                          onClick={(e) => { e.stopPropagation(); moveLead(lead, "forward"); }}
                          disabled={actionLoading}
                          className="p-1 rounded hover:bg-white/10 text-gray-500 disabled:opacity-50"
                        >
                          <ArrowRight className="w-3.5 h-3.5" />
                        </button>
                      )}
                    </div>
                  </div>
                ))}
                
                {stageLeads.length === 0 && (
                  <div className="text-center py-8 text-gray-600 text-xs">
                    No leads
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
