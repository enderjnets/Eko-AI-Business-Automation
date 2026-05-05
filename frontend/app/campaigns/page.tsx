"use client";

import { useState, useEffect } from "react";
import { Plus, Play, Pause, Loader2, Target, Pencil, Trash2, X } from "lucide-react";
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

  // Edit modal state
  const [editingCampaign, setEditingCampaign] = useState<Campaign | null>(null);
  const [editForm, setEditForm] = useState({
    name: "",
    description: "",
    status: "draft",
    email_subject_template: "",
    email_body_template: "",
    follow_up_delay_hours: 72,
    max_follow_ups: 3,
  });
  const [editLoading, setEditLoading] = useState(false);
  const [editError, setEditError] = useState<string | null>(null);

  // Delete confirmation state
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

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

  const openEdit = async (campaign: Campaign) => {
    setEditError(null);
    try {
      const res = await campaignsApi.get(campaign.id);
      const data = res.data;
      setEditForm({
        name: data.name || "",
        description: data.description || "",
        status: data.status || "draft",
        email_subject_template: data.email_subject_template || "",
        email_body_template: data.email_body_template || "",
        follow_up_delay_hours: data.follow_up_delay_hours ?? 72,
        max_follow_ups: data.max_follow_ups ?? 3,
      });
      setEditingCampaign(campaign);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSaveEdit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingCampaign) return;
    if (!editForm.name.trim()) {
      setEditError("El nombre es obligatorio");
      return;
    }
    setEditLoading(true);
    setEditError(null);
    try {
      await campaignsApi.update(editingCampaign.id, {
        name: editForm.name.trim(),
        description: editForm.description.trim() || undefined,
        status: editForm.status,
        email_subject_template: editForm.email_subject_template.trim() || undefined,
        email_body_template: editForm.email_body_template.trim() || undefined,
        follow_up_delay_hours: editForm.follow_up_delay_hours,
        max_follow_ups: editForm.max_follow_ups,
      });
      setEditingCampaign(null);
      loadCampaigns();
    } catch (err: any) {
      console.error(err);
      setEditError(err.response?.data?.detail || "Error guardando cambios");
    } finally {
      setEditLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("¿Eliminar esta campaña? Esta acción no se puede deshacer.")) return;
    setDeleteLoading(true);
    setDeletingId(id);
    try {
      await campaignsApi.delete(id);
      loadCampaigns();
    } catch (err) {
      console.error(err);
      alert("Error eliminando campaña");
    } finally {
      setDeleteLoading(false);
      setDeletingId(null);
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
                  <div className="min-w-0">
                    <h3 className="font-medium truncate">{campaign.name}</h3>
                    <p className="text-xs text-gray-500 mt-0.5 capitalize">
                      {campaign.campaign_type.replace("_", " ")} • {campaign.target_city}
                    </p>
                  </div>
                  <span className={`text-xs px-2 py-1 rounded-full capitalize shrink-0 ${getStatusColor(campaign.status)}`}>
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

                {/* Edit / Delete actions */}
                <div className="flex items-center justify-end gap-1 mt-3 pt-3 border-t border-white/5">
                  <button
                    onClick={() => openEdit(campaign)}
                    className="p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
                    title="Editar"
                  >
                    <Pencil className="w-3.5 h-3.5" />
                  </button>
                  <button
                    onClick={() => handleDelete(campaign.id)}
                    disabled={deleteLoading && deletingId === campaign.id}
                    className="p-1.5 rounded-lg text-gray-400 hover:text-red-400 hover:bg-red-500/10 transition-colors disabled:opacity-50"
                    title="Eliminar"
                  >
                    {deleteLoading && deletingId === campaign.id ? (
                      <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    ) : (
                      <Trash2 className="w-3.5 h-3.5" />
                    )}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      {/* Edit Modal */}
      {editingCampaign && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <div className="w-full max-w-lg rounded-xl border border-white/10 bg-eko-graphite shadow-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between px-5 py-4 border-b border-white/5">
              <h3 className="font-medium text-sm">Editar Campaña</h3>
              <button
                onClick={() => setEditingCampaign(null)}
                className="p-1 rounded-lg hover:bg-white/10 text-gray-400"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleSaveEdit} className="px-5 py-4 space-y-4">
              {editError && (
                <div className="rounded-lg bg-red-500/10 border border-red-500/20 px-3 py-2 text-sm text-red-400">
                  {editError}
                </div>
              )}

              <div>
                <label className="text-xs text-gray-500 mb-1 block">Nombre *</label>
                <input
                  type="text"
                  value={editForm.name}
                  onChange={(e) => setEditForm({ ...editForm, name: e.target.value })}
                  placeholder="Nombre de la campaña"
                  className="w-full rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm focus:border-eko-blue focus:outline-none"
                  required
                />
              </div>

              <div>
                <label className="text-xs text-gray-500 mb-1 block">Descripción</label>
                <textarea
                  value={editForm.description}
                  onChange={(e) => setEditForm({ ...editForm, description: e.target.value })}
                  placeholder="Descripción de la campaña..."
                  rows={2}
                  className="w-full rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm focus:border-eko-blue focus:outline-none resize-none"
                />
              </div>

              <div>
                <label className="text-xs text-gray-500 mb-1 block">Estado</label>
                <select
                  value={editForm.status}
                  onChange={(e) => setEditForm({ ...editForm, status: e.target.value })}
                  className="w-full rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm focus:border-eko-blue focus:outline-none"
                >
                  <option value="draft">Draft</option>
                  <option value="active">Active</option>
                  <option value="paused">Paused</option>
                  <option value="completed">Completed</option>
                  <option value="archived">Archived</option>
                </select>
              </div>

              <div>
                <label className="text-xs text-gray-500 mb-1 block">Asunto del email</label>
                <input
                  type="text"
                  value={editForm.email_subject_template}
                  onChange={(e) => setEditForm({ ...editForm, email_subject_template: e.target.value })}
                  placeholder="Ej: Quick question about your business"
                  className="w-full rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm focus:border-eko-blue focus:outline-none"
                />
              </div>

              <div>
                <label className="text-xs text-gray-500 mb-1 block">Cuerpo del email</label>
                <textarea
                  value={editForm.email_body_template}
                  onChange={(e) => setEditForm({ ...editForm, email_body_template: e.target.value })}
                  placeholder="Plantilla del cuerpo del email..."
                  rows={4}
                  className="w-full rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm focus:border-eko-blue focus:outline-none resize-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-xs text-gray-500 mb-1 block">Delay follow-up (horas)</label>
                  <input
                    type="number"
                    value={editForm.follow_up_delay_hours}
                    onChange={(e) => setEditForm({ ...editForm, follow_up_delay_hours: parseInt(e.target.value) || 0 })}
                    min={1}
                    className="w-full rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm focus:border-eko-blue focus:outline-none"
                  />
                </div>
                <div>
                  <label className="text-xs text-gray-500 mb-1 block">Max follow-ups</label>
                  <input
                    type="number"
                    value={editForm.max_follow_ups}
                    onChange={(e) => setEditForm({ ...editForm, max_follow_ups: parseInt(e.target.value) || 0 })}
                    min={0}
                    className="w-full rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm focus:border-eko-blue focus:outline-none"
                  />
                </div>
              </div>
            </form>

            <div className="flex items-center gap-2 px-5 py-4 border-t border-white/5">
              <button
                type="submit"
                onClick={handleSaveEdit}
                disabled={editLoading}
                className="flex-1 rounded-lg bg-eko-blue py-2.5 text-sm font-medium hover:bg-eko-blue-dark disabled:opacity-50 transition-colors"
              >
                {editLoading ? <Loader2 className="w-4 h-4 animate-spin mx-auto" /> : "Guardar Cambios"}
              </button>
              <button
                onClick={() => setEditingCampaign(null)}
                className="rounded-lg border border-white/10 px-4 py-2.5 text-sm text-gray-400 hover:bg-white/5 transition-colors"
              >
                Cancelar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
