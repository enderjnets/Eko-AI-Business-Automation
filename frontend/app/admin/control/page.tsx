"use client";

import { useState, useEffect, useCallback } from "react";
import Link from "next/link";
import {
  Server, Boxes, Activity, AlertTriangle, Plus, Loader2, X, RefreshCw,
} from "lucide-react";
import Navbar from "@/components/Navbar";
import StatCard from "@/components/StatCard";
import {
  controlPlaneApi, type ControlPlaneInstance, type ControlPlaneProduct,
} from "@/lib/api";

const STATUS_BADGE: Record<string, string> = {
  active: "bg-eko-green/10 text-eko-green border-eko-green/20",
  error: "bg-red-500/10 text-red-400 border-red-500/20",
  suspended: "bg-gray-500/10 text-gray-400 border-gray-500/20",
  provisioning: "bg-gold/10 text-gold border-gold/20",
  unknown: "bg-gray-500/10 text-gray-500 border-gray-500/20",
};

function StatusBadge({ status }: { status: string }) {
  return (
    <span className={`inline-block px-2 py-0.5 rounded text-xs border capitalize ${STATUS_BADGE[status] || STATUS_BADGE.unknown}`}>
      {status}
    </span>
  );
}

function timeAgo(iso?: string | null): string {
  if (!iso) return "never";
  const diff = Date.now() - new Date(iso).getTime();
  const m = Math.floor(diff / 60000);
  if (m < 1) return "just now";
  if (m < 60) return `${m}m ago`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}h ago`;
  return `${Math.floor(h / 24)}d ago`;
}

export default function ControlPlanePage() {
  const [stats, setStats] = useState<{ products: number; instances_total: number; instances_active: number; instances_down: number; incidents_24h: number } | null>(null);
  const [instances, setInstances] = useState<ControlPlaneInstance[]>([]);
  const [products, setProducts] = useState<ControlPlaneProduct[]>([]);
  const [loading, setLoading] = useState(true);
  const [showProduct, setShowProduct] = useState(false);
  const [showInstance, setShowInstance] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [s, i, p] = await Promise.all([
        controlPlaneApi.stats(),
        controlPlaneApi.listInstances(),
        controlPlaneApi.listProducts(),
      ]);
      setStats(s.data);
      setInstances(i.data);
      setProducts(p.data);
    } catch (e) {
      // surfaced via empty states
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  return (
    <div className="min-h-screen bg-eko-graphite">
      <Navbar />
      <main className="pt-20 pb-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-display font-bold flex items-center gap-2">
              <Server className="w-6 h-6 text-eko-blue" /> Control Plane
            </h1>
            <p className="text-sm text-gray-500 mt-1">Productos e instancias deployadas en producción</p>
          </div>
          <div className="flex items-center gap-2">
            <button onClick={load} className="p-2 rounded-lg text-gray-400 hover:text-white hover:bg-white/10" title="Refresh">
              <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
            </button>
            <button onClick={() => setShowProduct(true)} className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm border border-white/10 text-gray-300 hover:bg-white/5">
              <Plus className="w-4 h-4" /> Producto
            </button>
            <button onClick={() => setShowInstance(true)} className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm bg-eko-blue text-white hover:bg-eko-blue-dark">
              <Plus className="w-4 h-4" /> Instancia
            </button>
          </div>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <StatCard title="Productos" value={stats?.products ?? "—"} icon={Boxes} color="blue" />
          <StatCard title="Instancias activas" value={stats?.instances_active ?? "—"} subtitle={`${stats?.instances_total ?? 0} totales`} icon={Activity} color="green" />
          <StatCard title="Caídas" value={stats?.instances_down ?? "—"} icon={AlertTriangle} color="rose" />
          <StatCard title="Incidentes 24h" value={stats?.incidents_24h ?? "—"} icon={AlertTriangle} color="gold" />
        </div>

        <div className="rounded-xl border border-white/10 overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-white/5 text-gray-400">
              <tr>
                <th className="text-left px-4 py-3 font-medium">Cliente</th>
                <th className="text-left px-4 py-3 font-medium">Producto</th>
                <th className="text-left px-4 py-3 font-medium">Estado</th>
                <th className="text-left px-4 py-3 font-medium">Plan</th>
                <th className="text-left px-4 py-3 font-medium">URL</th>
                <th className="text-left px-4 py-3 font-medium">Último health</th>
              </tr>
            </thead>
            <tbody>
              {loading && (
                <tr><td colSpan={6} className="px-4 py-10 text-center text-gray-500"><Loader2 className="w-5 h-5 animate-spin inline" /></td></tr>
              )}
              {!loading && instances.length === 0 && (
                <tr><td colSpan={6} className="px-4 py-10 text-center text-gray-500">No hay instancias registradas todavía.</td></tr>
              )}
              {!loading && instances.map((inst) => (
                <tr key={inst.id} className="border-t border-white/5 hover:bg-white/5">
                  <td className="px-4 py-3">
                    <Link href={`/admin/control/${inst.id}`} className="text-white hover:text-eko-blue font-medium">{inst.client_name}</Link>
                  </td>
                  <td className="px-4 py-3 text-gray-400">{inst.product_name || inst.product_key || inst.product_id}</td>
                  <td className="px-4 py-3"><StatusBadge status={inst.status} /></td>
                  <td className="px-4 py-3 text-gray-400">{inst.plan || "—"}</td>
                  <td className="px-4 py-3 text-gray-500 truncate max-w-[200px]">{inst.base_url}</td>
                  <td className="px-4 py-3 text-gray-400">{timeAgo(inst.last_seen_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>

      {showProduct && <ProductModal products={products} onClose={() => setShowProduct(false)} onSaved={() => { setShowProduct(false); load(); }} />}
      {showInstance && <InstanceModal products={products} onClose={() => setShowInstance(false)} onSaved={() => { setShowInstance(false); load(); }} />}
    </div>
  );
}

function ModalShell({ title, onClose, children }: { title: string; onClose: () => void; children: React.ReactNode }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/60" onClick={onClose} />
      <div className="relative w-full max-w-lg rounded-xl border border-white/10 bg-eko-graphite p-6 max-h-[85vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-display font-semibold">{title}</h2>
          <button onClick={onClose} className="p-1 text-gray-400 hover:text-white"><X className="w-5 h-5" /></button>
        </div>
        {children}
      </div>
    </div>
  );
}

const inputCls = "w-full bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-eko-blue";
const labelCls = "block text-xs text-gray-400 mb-1";

function ProductModal({ onClose, onSaved }: { products: ControlPlaneProduct[]; onClose: () => void; onSaved: () => void }) {
  const [form, setForm] = useState({ key: "", name: "", description: "" });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async () => {
    setSaving(true); setError(null);
    try {
      await controlPlaneApi.createProduct({ key: form.key, name: form.name, description: form.description || undefined });
      onSaved();
    } catch (e: any) {
      setError(e?.response?.data?.detail || "Error al crear producto");
    } finally { setSaving(false); }
  };

  return (
    <ModalShell title="Nuevo producto" onClose={onClose}>
      <div className="space-y-3">
        <div><label className={labelCls}>Key (ej. realtors)</label><input className={inputCls} value={form.key} onChange={(e) => setForm({ ...form, key: e.target.value })} /></div>
        <div><label className={labelCls}>Nombre</label><input className={inputCls} value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></div>
        <div><label className={labelCls}>Descripción</label><textarea className={inputCls} rows={2} value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></div>
        {error && <p className="text-xs text-red-400">{error}</p>}
        <button disabled={saving || !form.key || !form.name} onClick={submit} className="w-full bg-eko-blue text-white rounded-lg py-2 text-sm font-medium disabled:opacity-50">
          {saving ? "Guardando..." : "Crear producto"}
        </button>
      </div>
    </ModalShell>
  );
}

function InstanceModal({ products, onClose, onSaved }: { products: ControlPlaneProduct[]; onClose: () => void; onSaved: () => void }) {
  const [form, setForm] = useState({ product_id: products[0]?.id ?? 0, client_name: "", base_url: "", agent_url: "", host: "", plan: "", service_key: "", agent_key: "", notes: "" });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async () => {
    setSaving(true); setError(null);
    try {
      await controlPlaneApi.createInstance({
        product_id: Number(form.product_id),
        client_name: form.client_name,
        base_url: form.base_url,
        agent_url: form.agent_url || undefined,
        host: form.host || undefined,
        plan: form.plan || undefined,
        service_key: form.service_key || undefined,
        agent_key: form.agent_key || undefined,
        notes: form.notes || undefined,
      });
      onSaved();
    } catch (e: any) {
      setError(e?.response?.data?.detail || "Error al crear instancia");
    } finally { setSaving(false); }
  };

  return (
    <ModalShell title="Nueva instancia (cliente)" onClose={onClose}>
      {products.length === 0 ? (
        <p className="text-sm text-gray-400">Primero registra un producto.</p>
      ) : (
        <div className="space-y-3">
          <div>
            <label className={labelCls}>Producto</label>
            <select className={inputCls} value={form.product_id} onChange={(e) => setForm({ ...form, product_id: Number(e.target.value) })}>
              {products.map((p) => <option key={p.id} value={p.id}>{p.name}</option>)}
            </select>
          </div>
          <div><label className={labelCls}>Cliente</label><input className={inputCls} value={form.client_name} onChange={(e) => setForm({ ...form, client_name: e.target.value })} /></div>
          <div><label className={labelCls}>Base URL (ej. http://100.x:8011)</label><input className={inputCls} value={form.base_url} onChange={(e) => setForm({ ...form, base_url: e.target.value })} /></div>
          <div><label className={labelCls}>Agent URL (opcional)</label><input className={inputCls} value={form.agent_url} onChange={(e) => setForm({ ...form, agent_url: e.target.value })} /></div>
          <div className="grid grid-cols-2 gap-3">
            <div><label className={labelCls}>Host</label><input className={inputCls} value={form.host} onChange={(e) => setForm({ ...form, host: e.target.value })} /></div>
            <div><label className={labelCls}>Plan</label><input className={inputCls} value={form.plan} onChange={(e) => setForm({ ...form, plan: e.target.value })} /></div>
          </div>
          <div><label className={labelCls}>Service key (X-Control-Key)</label><input className={inputCls} type="password" value={form.service_key} onChange={(e) => setForm({ ...form, service_key: e.target.value })} /></div>
          <div><label className={labelCls}>Agent key (X-Agent-Key)</label><input className={inputCls} type="password" value={form.agent_key} onChange={(e) => setForm({ ...form, agent_key: e.target.value })} /></div>
          {error && <p className="text-xs text-red-400">{error}</p>}
          <button disabled={saving || !form.client_name || !form.base_url} onClick={submit} className="w-full bg-eko-blue text-white rounded-lg py-2 text-sm font-medium disabled:opacity-50">
            {saving ? "Guardando..." : "Registrar instancia"}
          </button>
        </div>
      )}
    </ModalShell>
  );
}
