"use client";

import { useState, useEffect } from "react";
import { Star, MapPin, Mail, Phone, Globe, ArrowRight } from "lucide-react";
import { leadsApi } from "@/lib/api";
import Link from "next/link";

interface Lead {
  id: number;
  business_name: string;
  category: string;
  city: string;
  state: string;
  urgency_score: number;
  fit_score: number;
  total_score: number;
  status: string;
  email?: string;
  phone?: string;
  website?: string;
}

interface RecentLeadsProps {
  refreshTrigger?: number;
}

export default function RecentLeads({ refreshTrigger }: RecentLeadsProps) {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLeads();
  }, [refreshTrigger]);

  const loadLeads = async () => {
    try {
      const res = await leadsApi.list({ page_size: 10 });
      setLeads(res.data.items || []);
    } catch (err) {
      console.error("Failed to load leads:", err);
    } finally {
      setLoading(false);
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
      <div className="rounded-xl border border-white/5 bg-white/[0.02] p-6">
        <div className="animate-pulse space-y-3">
          {Array.from({ length: 5 }).map((_, i) => (
            <div key={i} className="h-16 bg-white/5 rounded-lg" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-white/5 bg-white/[0.02] p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold font-display">Leads Recientes</h2>
        <Link
          href="/leads"
          className="text-sm text-eko-blue hover:text-eko-blue-dark flex items-center gap-1 transition-colors"
        >
          Ver todos
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>

      {leads.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <p>No hay leads aún. Usa el formulario de Discovery para encontrar negocios.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {leads.map((lead) => (
            <div
              key={lead.id}
              className="flex items-center justify-between rounded-lg border border-white/5 bg-white/[0.02] p-4 hover:bg-white/[0.04] transition-colors"
            >
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <h3 className="font-medium text-sm truncate">{lead.business_name}</h3>
                  {lead.category && (
                    <span className="text-xs px-2 py-0.5 rounded-full bg-white/5 text-gray-400">
                      {lead.category}
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-3 mt-1.5 text-xs text-gray-500">
                  <span className="flex items-center gap-1">
                    <MapPin className="w-3 h-3" />
                    {lead.city}, {lead.state}
                  </span>
                  {lead.email && <Mail className="w-3 h-3" />}
                  {lead.phone && <Phone className="w-3 h-3" />}
                  {lead.website && <Globe className="w-3 h-3" />}
                </div>
              </div>

              <div className="flex items-center gap-4 ml-4">
                {lead.total_score > 0 && (
                  <div className="text-right">
                    <div className={`text-lg font-bold font-display ${getScoreColor(lead.total_score)}`}>
                      {Math.round(lead.total_score)}
                    </div>
                    <div className="text-xs text-gray-600">score</div>
                  </div>
                )}
                <span className="text-xs px-2 py-1 rounded-full bg-white/5 text-gray-400 capitalize">
                  {lead.status.replace("_", " ")}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
