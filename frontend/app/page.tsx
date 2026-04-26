"use client";

import { useState, useEffect } from "react";
import {
  Users,
  MailOpen,
  TrendingUp,
  Target,
  Zap,
} from "lucide-react";
import Navbar from "@/components/Navbar";
import StatCard from "@/components/StatCard";
import PipelineBoard from "@/components/PipelineBoard";
import DiscoveryForm from "@/components/DiscoveryForm";
import RecentLeads from "@/components/RecentLeads";
import { analyticsApi } from "@/lib/api";
import VersionBadge from "@/components/VersionBadge";

export default function Dashboard() {
  const [stats, setStats] = useState({
    total_leads: 0,
    contacted: 0,
    closed_won: 0,
    conversion_rate: 0,
    avg_lead_score: 0,
  });
  const [discoveryResult, setDiscoveryResult] = useState<any>(null);
  const [refreshLeads, setRefreshLeads] = useState(0);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const res = await analyticsApi.performance();
      setStats(res.data);
    } catch (err) {
      console.error("Failed to load stats:", err);
    }
  };

  return (
    <div className="min-h-screen bg-eko-graphite">
      <Navbar />

      <main className="pt-20 pb-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold font-display">
            Dashboard
          </h1>
          <p className="text-gray-400 text-sm mt-1">
            Sistema de Agentes Autónomos para Prospección y Ventas
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <StatCard
            title="Total Leads"
            value={stats.total_leads}
            subtitle="Leads en el sistema"
            icon={Users}
            color="blue"
          />
          <StatCard
            title="Contactados"
            value={stats.contacted}
            subtitle="Leads con contacto iniciado"
            icon={MailOpen}
            color="gold"
          />
          <StatCard
            title="Conversion Rate"
            value={`${stats.conversion_rate}%`}
            subtitle="Lead → Cliente"
            icon={TrendingUp}
            color="green"
          />
          <StatCard
            title="Avg Score"
            value={Math.round(stats.avg_lead_score)}
            subtitle="Puntuación promedio"
            icon={Target}
            color="rose"
          />
        </div>

        {/* Pipeline */}
        <div className="mb-8">
          <PipelineBoard />
        </div>

        {/* Discovery + Recent Leads */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1">
            <DiscoveryForm
              onSuccess={(data) => {
                setDiscoveryResult(data);
                loadStats();
                setRefreshLeads((prev) => prev + 1);
              }}
            />

            {discoveryResult && (
              <div className="mt-4 rounded-xl border border-eko-green/20 bg-eko-green/5 p-4">
                <div className="flex items-center gap-2 text-eko-green">
                  <Zap className="w-4 h-4" />
                  <span className="text-sm font-medium">
                    {discoveryResult.total} leads descubiertos
                  </span>
                </div>
              </div>
            )}
          </div>

          <div className="lg:col-span-2">
            <RecentLeads refreshTrigger={refreshLeads} />
          </div>
        </div>
      </main>

      <VersionBadge />
    </div>
  );
}
