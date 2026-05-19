"use client";

import { useState, useEffect, useCallback } from "react";
import Link from "next/link";
import { Plus, Play, Pause, Loader2, ArrowRight, Users, CheckCircle } from "lucide-react";
import Navbar from "@/components/Navbar";
import { useT } from "@/contexts/I18nProvider";
import { sequencesApi } from "@/lib/api";

interface Sequence {
  id: number;
  name: string;
  description: string | null;
  status: string;
  leads_entered: number;
  leads_completed: number;
  leads_converted: number;
  created_at: string;
}

export default function SequencesPage() {
  const [sequences, setSequences] = useState<Sequence[]>([]);
  const { t } = useT();
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [newName, setNewName] = useState("");
  const [newDescription, setNewDescription] = useState("");
  const [showCreate, setShowCreate] = useState(false);

  const loadSequences = useCallback(async () => {
    setLoading(true);
    try {
      const res = await sequencesApi.list();
      setSequences(res.data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadSequences();
  }, [loadSequences]);

  const handleCreate = async () => {
    if (!newName.trim()) return;
    setCreating(true);
    try {
      await sequencesApi.create({
        name: newName.trim(),
        description: newDescription.trim() || undefined,
      });
      setNewName("");
      setNewDescription("");
      setShowCreate(false);
      loadSequences();
    } catch (err) {
      console.error(err);
    } finally {
      setCreating(false);
    }
  };

  const handleActivate = async (id: number) => {
    try {
      await sequencesApi.update(id, { status: "active" });
      loadSequences();
    } catch (err) {
      console.error(err);
    }
  };

  const handlePause = async (id: number) => {
    try {
      await sequencesApi.update(id, { status: "paused" });
      loadSequences();
    } catch (err) {
      console.error(err);
    }
  };

  const statusColor = (status: string) => {
    switch (status) {
      case "active": return "text-eko-green bg-eko-green/10 border-eko-green/20";
      case "paused": return "text-gold bg-gold/10 border-gold/20";
      case "draft": return "text-gray-400 bg-gray-500/10 border-gray-500/20";
      case "completed": return "text-eko-blue bg-eko-blue/10 border-eko-blue/20";
      default: return "text-gray-400 bg-gray-500/10 border-gray-500/20";
    }
  };

  const statusLabel = (status: string) => {
    switch (status) {
      case "active": return t("sequences.status.active");
      case "paused": return t("sequences.status.paused");
      case "draft": return t("sequences.status.draft");
      case "completed": return t("sequences.status.completed");
      default: return status;
    }
  };

  return (
    <div className="min-h-screen bg-eko-graphite">
      <Navbar />
      <main className="pt-20 pb-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold font-display">{t("sequences.title")}</h1>
            <p className="text-gray-400 text-sm">{t("sequences.subtitle")}</p>
          </div>
          <button
            onClick={() => setShowCreate(true)}
            className="flex items-center gap-2 rounded-lg bg-eko-blue px-4 py-2 text-sm font-medium hover:bg-eko-blue-dark transition-colors"
          >
            <Plus className="w-4 h-4" />
            {t("sequences.new")}
          </button>
        </div>

        {showCreate && (
          <div className="mb-6 rounded-xl border border-white/5 bg-white/[0.02] p-4">
            <h3 className="text-sm font-medium mb-3">{t("sequences.create_new")}</h3>
            <div className="flex flex-col sm:flex-row gap-3">
              <input
                type="text"
                value={newName}
                onChange={(e) => setNewName(e.target.value)}
                placeholder={t("sequences.name_placeholder")}
                className="flex-1 rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm focus:border-eko-blue focus:outline-none"
              />
              <input
                type="text"
                value={newDescription}
                onChange={(e) => setNewDescription(e.target.value)}
                placeholder={t("sequences.description_placeholder")}
                className="flex-1 rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm focus:border-eko-blue focus:outline-none"
              />
              <div className="flex gap-2">
                <button
                  onClick={handleCreate}
                  disabled={creating || !newName.trim()}
                  className="rounded-lg bg-eko-blue px-4 py-2 text-sm font-medium hover:bg-eko-blue-dark disabled:opacity-50 transition-colors"
                >
                  {creating ? <Loader2 className="w-4 h-4 animate-spin" /> : t("sequences.create")}
                </button>
                <button
                  onClick={() => setShowCreate(false)}
                  className="rounded-lg border border-white/10 px-4 py-2 text-sm text-gray-400 hover:bg-white/5 transition-colors"
                >
                  {t("common.cancel")}
                </button>
              </div>
            </div>
          </div>
        )}

        {loading ? (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="w-6 h-6 animate-spin text-eko-blue" />
          </div>
        ) : sequences.length === 0 ? (
          <div className="text-center py-20 text-gray-500">
            <p>{t("sequences.empty")}</p>
            <p className="text-sm mt-1">{t("sequences.empty_hint")}</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {sequences.map((seq) => (
              <div
                key={seq.id}
                className="rounded-xl border border-white/5 bg-white/[0.02] p-5 hover:border-white/10 transition-colors"
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-medium text-sm">{seq.name}</h3>
                    {seq.description && (
                      <p className="text-xs text-gray-500 mt-1">{seq.description}</p>
                    )}
                  </div>
                  <span className={`text-xs px-2 py-1 rounded-full border capitalize ${statusColor(seq.status)}`}>
                    {statusLabel(seq.status)}
                  </span>
                </div>

                <div className="flex items-center gap-4 mb-4 text-xs text-gray-400">
                  <span className="flex items-center gap-1">
                    <Users className="w-3 h-3" />
                    {seq.leads_entered} {t("sequences.enrolled")}
                  </span>
                  <span className="flex items-center gap-1">
                    <CheckCircle className="w-3 h-3" />
                    {seq.leads_completed} {t("sequences.completed_short")}
                  </span>
                </div>

                <div className="flex items-center gap-2">
                  {seq.status === "draft" || seq.status === "paused" ? (
                    <button
                      onClick={() => handleActivate(seq.id)}
                      className="flex items-center gap-1 rounded-lg bg-eko-green/20 border border-eko-green/30 px-3 py-1.5 text-xs font-medium text-eko-green hover:bg-eko-green/30 transition-colors"
                    >
                      <Play className="w-3 h-3" />
                      {t("sequences.activate")}
                    </button>
                  ) : (
                    <button
                      onClick={() => handlePause(seq.id)}
                      className="flex items-center gap-1 rounded-lg bg-gold/20 border border-gold/30 px-3 py-1.5 text-xs font-medium text-gold hover:bg-gold/30 transition-colors"
                    >
                      <Pause className="w-3 h-3" />
                      {t("sequences.pause")}
                    </button>
                  )}
                  <Link
                    href={`/sequences/${seq.id}`}
                    className="flex items-center gap-1 rounded-lg border border-white/10 px-3 py-1.5 text-xs text-gray-300 hover:bg-white/5 transition-colors ml-auto"
                  >
                    {t("common.edit")}
                    <ArrowRight className="w-3 h-3" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
