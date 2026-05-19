"use client";

import { useState, useEffect } from "react";
import {
  Users,
  MailOpen,
  TrendingUp,
  Target,
  Zap,
  BarChart3,
  GitBranch,
  Briefcase,
  Inbox,
  ListOrdered,
  Mail,
  Calendar,
  Settings,
  FileText,
  Mic,
  Clapperboard,
  LayoutTemplate,
  CreditCard,
  Loader2,
} from "lucide-react";
import Navbar from "@/components/Navbar";
import StatCard from "@/components/StatCard";
import PipelineBoard from "@/components/PipelineBoard";
import DiscoveryForm from "@/components/DiscoveryForm";
import RecentLeads from "@/components/RecentLeads";
import ModulesGrid, { type ModuleDef } from "@/components/ModulesGrid";
import { analyticsApi, emailsApi, dealsApi } from "@/lib/api";
import { useT } from "@/contexts/I18nProvider";
import type { TranslationKey } from "@/lib/i18n/translations";


// Default order follows a logical sales funnel: ACQUIRE → ENGAGE → CLOSE → GROW → OPS.
// label + subtitle are translation keys resolved at render time by ModulesGrid.
const MODULES: ModuleDef[] = [
  // 1. Acquire — leads enter the system
  { href: "/leads", label: "modules.leads.label", subtitle: "modules.leads.subtitle", icon: Users, color: "text-eko-blue bg-eko-blue/10 border-eko-blue/20" },
  { href: "/landing-pages", label: "modules.landing_pages.label", subtitle: "modules.landing_pages.subtitle", icon: LayoutTemplate, color: "text-sky-400 bg-sky-500/10 border-sky-500/20" },
  // 2. Engage — talk to them
  { href: "/inbox", label: "modules.inbox.label", subtitle: "modules.inbox.subtitle", icon: Inbox, color: "text-rose bg-rose/10 border-rose/20", badgeKey: "unread" },
  { href: "/sequences", label: "modules.sequences.label", subtitle: "modules.sequences.subtitle", icon: ListOrdered, color: "text-purple-400 bg-purple-500/10 border-purple-500/20" },
  { href: "/campaigns", label: "modules.campaigns.label", subtitle: "modules.campaigns.subtitle", icon: Mail, color: "text-cyan-400 bg-cyan-500/10 border-cyan-500/20" },
  { href: "/voice-agent", label: "modules.voice.label", subtitle: "modules.voice.subtitle", icon: Mic, color: "text-teal-400 bg-teal-500/10 border-teal-500/20" },
  { href: "/calendar", label: "modules.calendar.label", subtitle: "modules.calendar.subtitle", icon: Calendar, color: "text-orange-400 bg-orange-500/10 border-orange-500/20" },
  // 3. Close — convert
  { href: "/pipeline", label: "modules.pipeline.label", subtitle: "modules.pipeline.subtitle", icon: GitBranch, color: "text-eko-green bg-eko-green/10 border-eko-green/20" },
  { href: "/deals", label: "modules.deals.label", subtitle: "modules.deals.subtitle", icon: Briefcase, color: "text-gold bg-gold/10 border-gold/20" },
  { href: "/proposals", label: "modules.proposals.label", subtitle: "modules.proposals.subtitle", icon: FileText, color: "text-indigo-400 bg-indigo-500/10 border-indigo-500/20" },
  // 4. Grow — marketing + insights
  { href: "/content-studio", label: "modules.content.label", subtitle: "modules.content.subtitle", icon: Clapperboard, color: "text-pink-400 bg-pink-500/10 border-pink-500/20" },
  { href: "/analytics", label: "modules.analytics.label", subtitle: "modules.analytics.subtitle", icon: BarChart3, color: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20" },
  // 5. Ops — admin
  { href: "/billing", label: "modules.billing.label", subtitle: "modules.billing.subtitle", icon: CreditCard, color: "text-amber-400 bg-amber-500/10 border-amber-500/20" },
  { href: "/settings", label: "modules.settings.label", subtitle: "modules.settings.subtitle", icon: Settings, color: "text-gray-300 bg-gray-500/10 border-gray-500/20" },
];

export default function Dashboard() {
  const { t } = useT();
  const [stats, setStats] = useState({
    total_leads: 0,
    contacted: 0,
    closed_won: 0,
    conversion_rate: 0,
    avg_lead_score: 0,
  });
  const [discoveryResult, setDiscoveryResult] = useState<any>(null);
  const [refreshLeads, setRefreshLeads] = useState(0);
  const [unreadCount, setUnreadCount] = useState(0);
  const [dealsForecast, setDealsForecast] = useState<any>(null);
  const [loadingModules, setLoadingModules] = useState(true);

  useEffect(() => {
    loadStats();
    loadUnread();
    loadForecast();
  }, []);

  const loadStats = async () => {
    try {
      const res = await analyticsApi.performance();
      setStats(res.data);
    } catch (err) {
      console.error("Failed to load stats:", err);
    }
  };

  const loadUnread = async () => {
    try {
      const res = await emailsApi.inbox({ status: "unread", limit: 1 });
      setUnreadCount(res.data?.unread_count || 0);
    } catch {
      // silently fail
    } finally {
      setLoadingModules(false);
    }
  };

  const loadForecast = async () => {
    try {
      const res = await dealsApi.forecast();
      setDealsForecast(res.data);
    } catch {
      // silently fail
    }
  };

  return (
    <div className="min-h-screen bg-eko-graphite">
      <Navbar />

      <main className="pt-20 pb-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold font-display">{t("dashboard.title")}</h1>
          <p className="text-gray-400 text-sm mt-1">
            {t("dashboard.subtitle")}
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <StatCard
            title={t("dashboard.stats.total_leads")}
            value={stats.total_leads}
            subtitle={t("dashboard.stats.total_leads_sub")}
            icon={Users}
            color="blue"
          />
          <StatCard
            title={t("dashboard.stats.contacted")}
            value={stats.contacted}
            subtitle={t("dashboard.stats.contacted_sub")}
            icon={MailOpen}
            color="gold"
          />
          <StatCard
            title={t("dashboard.stats.conversion_rate")}
            value={`${stats.conversion_rate}%`}
            subtitle={t("dashboard.stats.conversion_rate_sub")}
            icon={TrendingUp}
            color="green"
          />
          <StatCard
            title={t("dashboard.stats.avg_score")}
            value={Math.round(stats.avg_lead_score)}
            subtitle={t("dashboard.stats.avg_score_sub")}
            icon={Target}
            color="rose"
          />
        </div>

        {/* Quick Access Modules — drag-and-drop reorder, add/remove */}
        <div className="mb-8">
          {dealsForecast && dealsForecast.total_weighted_value > 0 && (
            <div className="flex justify-end mb-1">
              <span className="text-xs text-gray-500">
                {t("dashboard.forecast")}: ${dealsForecast.total_weighted_value.toLocaleString("en-US")}
              </span>
            </div>
          )}
          {loadingModules ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="w-6 h-6 animate-spin text-eko-blue" />
            </div>
          ) : (
            <ModulesGrid modules={MODULES} unreadCount={unreadCount} />
          )}
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
                    {t("dashboard.discovery_success", { count: discoveryResult.total })}
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


    </div>
  );
}
