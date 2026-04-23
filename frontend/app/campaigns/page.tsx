"use client";

import { useState, useEffect } from "react";
import { Plus, Play, Pause, Loader2, Target } from "lucide-react";
import Navbar from "@/components/Navbar";
import { campaignsApi } from "@/lib/api";

interface Campaign {
  id: number;
  name: string;
  campaign_type: string;
  status: string;
  target_city: string;
  leads_total: number;
  leads_contacted: number;
  leads_responded: number;
  created_at: string;
}

export default function CampaignsPage() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionId, setActionId] = useState<number | null>(null);

  useEffect(() => {
    loadCampaigns();
  }, []);

  const loadCampaigns = async () => {
    try {
      const res = await campaignsApi.list();
      setCampaigns(res.data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleLaunch = async (id: number) => {
    setActionId(id);
    try {
      await campaignsApi.launch(id);
      loadCampaigns();
    } catch (err) {
      console.error(err);
    } finally {
      setActionId(null);
    }
  };

  const handlePause = async (id: number) => {
    setActionId(id);
    try {
      await campaignsApi.pause(id);
      loadCampaigns();
    } catch (err) {
      console.error(err);
    } finally {
      setActionId(null);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "active": return "text-eko-green bg-eko-green/10";
      case "paused": return "text-gold bg-gold/10";
      case "draft": return "text-gray-400 bg-white/5";
      case "completed": return "text-blue-400 bg-blue-400/10";
      default: return "text-gray-400 bg-white/5";
    }
  };

  return (
    <div className="min-h-screen bg-eko-graphite">
      <Navbar />
      <main className="pt-20 pb-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold font-display">Campañas</h1>
            <p className="text-gray-400 text-sm">Gestiona tus campañas de outreach</p>
          </div>
          <button className="flex items-center gap-2 rounded-lg bg-eko-blue px-4 py-2.5 text-sm font-medium hover:bg-eko-blue-dark transition-colors">
            <Plus className="w-4 h-4" />
            Nueva Campaña
          </button>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="w-8 h-8 animate-spin text-eko-blue" />
          </div>
        ) : campaigns.length === 0 ? (
          <div className="rounded-xl border border-white/5 bg-white/[0.02] p-12 text-center">
            <Target className="w-12 h-12 text-gray-600 mx-auto mb-4" />
            <h3 className="text-lg font-medium mb-2">No hay campañas aún</h3>
            <p className="text-gray-500 text-sm mb-4">
              Crea tu primera campaña para empezar a contactar leads.
            </p>
            <button className="flex items-center gap-2 mx-auto rounded-lg bg-eko-blue px-4 py-2.5 text-sm font-medium hover:bg-eko-blue-dark transition-colors">
              <Plus className="w-4 h-4" />
              Crear Campaña
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {campaigns.map((campaign) => (
              <div
                key={campaign.id}
                className="rounded-xl border border-white/5 bg-white/[0.02] p-5 hover:bg-white/[0.04] transition-colors"
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-medium">{campaign.name}</h3>
                    <p className="text-xs text-gray-500 mt-0.5 capitalize">
                      {campaign.campaign_type.replace("_", " ")} • {campaign.target_city}
                    </p>
                  </div>
                  <span className={`text-xs px-2 py-1 rounded-full capitalize ${getStatusColor(campaign.status)}`}>
                    {campaign.status}
                  </span>
                </div>

                <div className="grid grid-cols-3 gap-3 mb-4">
                  <div className="text-center">
                    <p className="text-lg font-bold font-display">{campaign.leads_total}</p>
                    <p className="text-xs text-gray-500">Leads</p>
                  </div>
                  <div className="text-center">
                    <p className="text-lg font-bold font-display">{campaign.leads_contacted}</p>
                    <p className="text-xs text-gray-500">Contactados</p>
                  </div>
                  <div className="text-center">
                    <p className="text-lg font-bold font-display">{campaign.leads_responded}</p>
                    <p className="text-xs text-gray-500">Respuestas</p>
                  </div>
                </div>

                <div className="flex gap-2">
                  {campaign.status === "draft" && (
                    <button
                      onClick={() => handleLaunch(campaign.id)}
                      disabled={actionId === campaign.id}
                      className="flex-1 flex items-center justify-center gap-1.5 rounded-lg bg-eko-green/10 text-eko-green px-3 py-2 text-sm font-medium hover:bg-eko-green/20 disabled:opacity-50 transition-colors"
                    >
                      {actionId === campaign.id ? (
                        <Loader2 className="w-3.5 h-3.5 animate-spin" />
                      ) : (
                        <Play className="w-3.5 h-3.5" />
                      )}
                      Lanzar
                    </button>
                  )}
                  {campaign.status === "active" && (
                    <button
                      onClick={() => handlePause(campaign.id)}
                      disabled={actionId === campaign.id}
                      className="flex-1 flex items-center justify-center gap-1.5 rounded-lg bg-gold/10 text-gold px-3 py-2 text-sm font-medium hover:bg-gold/20 disabled:opacity-50 transition-colors"
                    >
                      {actionId === campaign.id ? (
                        <Loader2 className="w-3.5 h-3.5 animate-spin" />
                      ) : (
                        <Pause className="w-3.5 h-3.5" />
                      )}
                      Pausar
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
