"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useT } from "@/contexts/I18nProvider";
import { voiceAgentApi, leadsApi } from "@/lib/api";
import {
  Phone,
  PhoneCall,
  Play,
  Loader2,
  AlertCircle,
  Clock,
  CheckCircle,
  XCircle,
  Voicemail,
  User,
  Settings,
  Plus,
  Search,
  Mic,
  BarChart3,
  ChevronRight,
  ExternalLink,
} from "lucide-react";

interface VoiceCall {
  id: number;
  lead_id: number;
  lead_name: string | null;
  lead_phone: string | null;
  result: string;
  notes: string | null;
  interest_level: string | null;
  next_action: string | null;
  call_duration_seconds: number | null;
  scheduled_at: string | null;
  completed_at: string | null;
  created_at: string;
}

const resultConfig: Record<string, { labelKey: string; color: string; icon: any }> = {
  SCHEDULED: { labelKey: "voice.result.scheduled", color: "text-amber-400", icon: Clock },
  INITIATED: { labelKey: "voice.result.initiated", color: "text-blue-400", icon: PhoneCall },
  COMPLETED: { labelKey: "voice.result.completed", color: "text-green-400", icon: CheckCircle },
  VOICEMAIL: { labelKey: "voice.result.voicemail", color: "text-purple-400", icon: Voicemail },
  NO_ANSWER: { labelKey: "voice.result.no_answer", color: "text-gray-400", icon: XCircle },
  BUSY: { labelKey: "voice.result.busy", color: "text-orange-400", icon: Phone },
  FAILED: { labelKey: "voice.result.failed", color: "text-red-400", icon: AlertCircle },
};

export default function VoiceAgentPage() {
  const router = useRouter();
  const [calls, setCalls] = useState<VoiceCall[]>([]);
  const { t } = useT();
  const [loading, setLoading] = useState(true);
  const [configLoading, setConfigLoading] = useState(true);
  const [config, setConfig] = useState({ configured: false });
  const [leads, setLeads] = useState<any[]>([]);
  const [searchLead, setSearchLead] = useState("");
  const [showCallModal, setShowCallModal] = useState(false);
  const [selectedLead, setSelectedLead] = useState<number | null>(null);
  const [callInstructions, setCallInstructions] = useState("");
  const [startingCall, setStartingCall] = useState(false);
  const [error, setError] = useState("");
  const [statusFilter, setStatusFilter] = useState("");

  useEffect(() => {
    loadCalls();
    loadConfig();
    loadLeads();
  }, []);

  async function loadCalls() {
    setLoading(true);
    try {
      const res = await voiceAgentApi.listCalls({ limit: 100 });
      setCalls(res.data.items || []);
    } catch (e: any) {
      setError(e.response?.data?.detail || t("voice.error.load"));
    } finally {
      setLoading(false);
    }
  }

  async function loadConfig() {
    setConfigLoading(true);
    try {
      const res = await voiceAgentApi.getConfig();
      setConfig(res.data);
    } catch {}
    setConfigLoading(false);
  }

  async function loadLeads() {
    try {
      const res = await leadsApi.list({ page_size: 200 });
      setLeads(res.data.items || []);
    } catch {}
  }

  async function handleStartCall() {
    if (!selectedLead) return;
    setStartingCall(true);
    setError("");
    try {
      await voiceAgentApi.startCall({
        lead_id: selectedLead,
        custom_instructions: callInstructions || undefined,
        schedule_now: true,
      });
      setShowCallModal(false);
      setSelectedLead(null);
      setCallInstructions("");
      loadCalls();
    } catch (e: any) {
      setError(e.response?.data?.detail || t("voice.error.start"));
    } finally {
      setStartingCall(false);
    }
  }

  const filteredLeads = leads.filter((l) =>
    !searchLead ||
    l.business_name?.toLowerCase().includes(searchLead.toLowerCase()) ||
    l.phone?.includes(searchLead)
  );

  const filteredCalls = calls.filter((c) =>
    !statusFilter || c.result === statusFilter
  );

  const stats = {
    total: calls.length,
    completed: calls.filter((c) => c.result === "COMPLETED").length,
    voicemail: calls.filter((c) => c.result === "VOICEMAIL").length,
    no_answer: calls.filter((c) => c.result === "NO_ANSWER").length,
    high_interest: calls.filter((c) => c.interest_level === "HIGH").length,
  };

  const formatDuration = (seconds: number | null) => {
    if (!seconds) return "0:00";
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s.toString().padStart(2, "0")}`;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{t("voice.title")}</h1>
            <p className="text-sm text-gray-500 mt-1">
              {t("voice.subtitle")}
            </p>
          </div>
          <div className="flex items-center gap-3">
            {!configLoading && !config.configured && (
              <div className="flex items-center gap-2 px-3 py-1.5 bg-amber-50 text-amber-700 rounded-lg text-sm">
                <AlertCircle className="w-4 h-4" />
                {t("voice.warn.no_api_key")}
              </div>
            )}
            <button
              onClick={() => setShowCallModal(true)}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <PhoneCall className="w-4 h-4" />
              {t("voice.new_call")}
            </button>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-6">
          {[
            { label: t("voice.stats.total"), value: stats.total, color: "bg-gray-100" },
            { label: t("voice.stats.completed"), value: stats.completed, color: "bg-green-50" },
            { label: t("voice.stats.voicemail"), value: stats.voicemail, color: "bg-purple-50" },
            { label: t("voice.stats.no_answer"), value: stats.no_answer, color: "bg-gray-50" },
            { label: t("voice.stats.high_interest"), value: stats.high_interest, color: "bg-blue-50" },
          ].map((s) => (
            <div key={s.label} className={`${s.color} rounded-xl p-4`}>
              <p className="text-2xl font-bold text-gray-900">{s.value}</p>
              <p className="text-sm text-gray-600">{s.label}</p>
            </div>
          ))}
        </div>

        {/* Filters */}
        <div className="flex flex-col sm:flex-row gap-3 mb-4">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="">{t("voice.filter.all_results")}</option>
            <option value="COMPLETED">{t("voice.result.completed")}</option>
            <option value="VOICEMAIL">{t("voice.result.voicemail")}</option>
            <option value="NO_ANSWER">{t("voice.result.no_answer")}</option>
            <option value="BUSY">{t("voice.result.busy")}</option>
            <option value="FAILED">{t("voice.result.failed")}</option>
            <option value="SCHEDULED">{t("voice.result.scheduled")}</option>
          </select>
        </div>

        {/* Error */}
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2 text-red-700 text-sm">
            <AlertCircle className="w-4 h-4" />
            {error}
          </div>
        )}

        {/* Calls List */}
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
          </div>
        ) : filteredCalls.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-xl border border-gray-200">
            <Phone className="w-12 h-12 text-gray-300 mx-auto mb-3" />
            <p className="text-gray-500">{t("voice.empty")}</p>
            <button
              onClick={() => setShowCallModal(true)}
              className="mt-2 text-blue-600 hover:text-blue-700 text-sm font-medium"
            >
              {t("voice.empty_cta")}
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            {filteredCalls.map((call) => {
              const cfg = resultConfig[call.result] || resultConfig.SCHEDULED;
              const Icon = cfg.icon;
              return (
                <div
                  key={call.id}
                  className="bg-white rounded-xl border border-gray-200 p-4 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium ${cfg.color}`}>
                          <Icon className="w-3 h-3" />
                          {t(cfg.labelKey as any)}
                        </span>
                        {call.interest_level && (
                          <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                            call.interest_level === "HIGH"
                              ? "bg-green-100 text-green-700"
                              : call.interest_level === "MEDIUM"
                              ? "bg-amber-100 text-amber-700"
                              : "bg-gray-100 text-gray-600"
                          }`}>
                            {t("voice.interest")}: {call.interest_level}
                          </span>
                        )}
                      </div>
                      <h3 className="font-semibold text-gray-900">
                        {call.lead_name || t("voice.unknown_lead")}
                      </h3>
                      <p className="text-sm text-gray-500">
                        {call.lead_phone || t("voice.no_phone")}
                        {call.call_duration_seconds ? ` · ${formatDuration(call.call_duration_seconds)}` : ""}
                      </p>
                      {call.notes && (
                        <p className="text-sm text-gray-600 mt-2 line-clamp-2">
                          {call.notes}
                        </p>
                      )}
                      <p className="text-xs text-gray-400 mt-1">
                        {new Date(call.created_at).toLocaleString("es-MX")}
                      </p>
                    </div>
                    <div className="flex items-center gap-1 ml-4">
                      <button
                        onClick={() => router.push(`/leads/${call.lead_id}`)}
                        title={t("voice.action.view_lead")}
                        className="p-2 text-gray-500 hover:bg-gray-100 rounded-lg transition-colors"
                      >
                        <ChevronRight className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Start Call Modal */}
      {showCallModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl p-6 w-full max-w-lg">
            <h2 className="text-lg font-bold text-gray-900 mb-4">
              {t("voice.modal.title")}
            </h2>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t("voice.modal.search_lead")}
                </label>
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <input
                    type="text"
                    placeholder={t("voice.modal.search_placeholder")}
                    value={searchLead}
                    onChange={(e) => setSearchLead(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>

              <div className="max-h-48 overflow-y-auto border border-gray-200 rounded-lg">
                {filteredLeads.length === 0 ? (
                  <p className="p-3 text-sm text-gray-500 text-center">{t("voice.modal.no_leads")}</p>
                ) : (
                  filteredLeads.map((lead) => (
                    <button
                      key={lead.id}
                      onClick={() => setSelectedLead(lead.id)}
                      className={`w-full text-left px-3 py-2 text-sm border-b border-gray-100 last:border-0 transition-colors ${
                        selectedLead === lead.id
                          ? "bg-blue-50 text-blue-700"
                          : "hover:bg-gray-50 text-gray-700"
                      }`}
                    >
                      <div className="font-medium">{lead.business_name}</div>
                      <div className="text-xs text-gray-500">{lead.phone || t("voice.no_phone")} · {lead.city || ""}</div>
                    </button>
                  ))
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t("voice.modal.instructions")}
                </label>
                <textarea
                  value={callInstructions}
                  onChange={(e) => setCallInstructions(e.target.value)}
                  placeholder={t("voice.modal.instructions_placeholder")}
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm"
                />
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button
                onClick={() => setShowCallModal(false)}
                className="flex-1 px-4 py-2 border border-gray-200 text-gray-700 rounded-lg hover:bg-gray-50"
              >
                {t("common.cancel")}
              </button>
              <button
                onClick={handleStartCall}
                disabled={startingCall || !selectedLead}
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center justify-center gap-2"
              >
                {startingCall ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <PhoneCall className="w-4 h-4" />
                )}
                {startingCall ? t("voice.modal.starting") : t("voice.modal.call")}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
