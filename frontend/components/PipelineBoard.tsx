"use client";

import { useState, useEffect } from "react";
import { analyticsApi } from "@/lib/api";

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

export default function PipelineBoard() {
  const [pipeline, setPipeline] = useState<Record<string, number>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPipeline();
  }, []);

  const loadPipeline = async () => {
    try {
      const res = await analyticsApi.pipeline();
      setPipeline(res.data.pipeline || {});
    } catch (err) {
      console.error("Failed to load pipeline:", err);
    } finally {
      setLoading(false);
    }
  };

  const total = Object.values(pipeline).reduce((a, b) => a + b, 0);

  if (loading) {
    return (
      <div className="rounded-xl border border-white/5 bg-white/[0.02] p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-white/10 rounded w-1/4" />
          <div className="grid grid-cols-5 gap-3">
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="h-24 bg-white/5 rounded-lg" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-white/5 bg-white/[0.02] p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold font-display">Pipeline de Ventas</h2>
        <span className="text-sm text-gray-500">{total} leads totales</span>
      </div>
      
      <div className="grid grid-cols-2 md:grid-cols-5 lg:grid-cols-10 gap-3">
        {PIPELINE_STAGES.map((stage) => {
          const count = pipeline[stage.key] || 0;
          const percentage = total > 0 ? (count / total) * 100 : 0;
          
          return (
            <div
              key={stage.key}
              className="relative rounded-lg border border-white/5 bg-white/[0.03] p-3 text-center hover:bg-white/[0.05] transition-colors"
            >
              <div className={`w-full h-1 rounded-full ${stage.color} mb-3 opacity-60`} />
              <p className="text-2xl font-bold font-display">{count}</p>
              <p className="text-xs text-gray-500 mt-1">{stage.label}</p>
              {percentage > 0 && (
                <p className="text-xs text-gray-600 mt-1">{percentage.toFixed(0)}%</p>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
