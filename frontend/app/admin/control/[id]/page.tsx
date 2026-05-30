"use client";

import { useState, useEffect, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import {
  ArrowLeft, Server, RefreshCw, Loader2, Play, Database, Rocket,
  FileText, AlertTriangle,
} from "lucide-react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";
import Navbar from "@/components/Navbar";
import { controlPlaneApi, type ControlPlaneActionLog } from "@/lib/api";

const STATUS_BADGE: Record<string, string> = {
  active: "bg-eko-green/10 text-eko-green border-eko-green/20",
  error: "bg-red-500/10 text-red-400 border-red-500/20",
  suspended: "bg-gray-500/10 text-gray-400 border-gray-500/20",
  provisioning: "bg-gold/10 text-gold border-gold/20",
  unknown: "bg-gray-500/10 text-gray-500 border-gray-500/20",
};

const ACTION_BADGE: Record<string, string> = {
  success: "text-eko-green",
  error: "text-red-400",
  running: "text-gold",
  pending: "text-gray-400",
};

type ActionType = "restart" | "migrate" | "redeploy";

export default function InstanceDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = Number(params.id);

  const [inst, setInst] = useState<any>(null);
  const [actions, setActions] = useState<ControlPlaneActionLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [logs, setLogs] = useState<string>("");
  const [logsLoading, setLogsLoading] = useState(false);
  const [confirm, setConfirm] = useState<ActionType | null>(null);
  const [running, setRunning] = useState(false);

  const load = useCallback(async () => {
    try {
      const [d, a] = await Promise.all([
        controlPlaneApi.getInstance(id),
        controlPlaneApi.listActions(id),
      ]);
      setInst(d.data);
      setActions(a.data);
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => { load(); }, [load]);

  const pollNow = async () => {
    setLoading(true);
    try { await controlPlaneApi.pollHealth(id); } catch {}
    await load();
  };

  const fetchLogs = async () => {
    setLogsLoading(true);
    try {
      const res = await controlPlaneApi.logs(id, { lines: 200 });
      setLogs(res.data.error ? `⚠ ${res.data.error}` : (res.data.output || "(sin salida)"));
    } catch {
      setLogs("⚠ No se pudieron obtener logs (agente inalcanzable)");
    } finally { setLogsLoading(false); }
  };

  const runAction = async (action: ActionType) => {
    setRunning(true); setConfirm(null);
    try {
      await controlPlaneApi.triggerAction(id, action);
      // Poll the audit list a few times so the result surfaces.
      for (let i = 0; i < 10; i++) {
        await new Promise((r) => setTimeout(r, 2000));
        const a = await controlPlaneApi.listActions(id);
        setActions(a.data);
        if (a.data[0] && ["success", "error"].includes(a.data[0].status)) break;
      }
    } finally { setRunning(false); }
  };

  if (loading && !inst) {
    return (
      <div className="min-h-screen bg-eko-graphite"><Navbar />
        <main className="pt-20 flex justify-center"><Loader2 className="w-6 h-6 animate-spin text-gray-500" /></main>
      </div>
    );
  }

  const latencyData = (inst?.recent_health || [])
    .slice().reverse()
    .map((h: any) => ({ t: new Date(h.checked_at).toLocaleTimeString(), latency: h.latency_ms ? Math.round(h.latency_ms) : 0, ok: h.ok }));

  const metrics = inst?.metrics;

  return (
    <div className="min-h-screen bg-eko-graphite">
      <Navbar />
      <main className="pt-20 pb-12 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto">
        <button onClick={() => router.push("/admin/control")} className="flex items-center gap-2 text-sm text-gray-400 hover:text-white mb-4">
          <ArrowLeft className="w-4 h-4" /> Volver
        </button>

        {/* Header */}
        <div className="flex items-start justify-between mb-6">
          <div>
            <h1 className="text-2xl font-display font-bold flex items-center gap-2">
              <Server className="w-6 h-6 text-eko-blue" /> {inst?.client_name}
            </h1>
            <p className="text-sm text-gray-500 mt-1">
              {inst?.product_name} · {inst?.base_url}
            </p>
          </div>
          <div className="flex items-center gap-3">
            <span className={`px-2.5 py-1 rounded text-xs border capitalize ${STATUS_BADGE[inst?.status] || STATUS_BADGE.unknown}`}>{inst?.status}</span>
            <button onClick={pollNow} className="p-2 rounded-lg text-gray-400 hover:text-white hover:bg-white/10" title="Poll ahora">
              <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
            </button>
          </div>
        </div>

        {/* Actions */}
        <div className="flex flex-wrap items-center gap-3 mb-8">
          <ActionButton icon={Play} label="Reiniciar" onClick={() => setConfirm("restart")} disabled={running} />
          <ActionButton icon={Database} label="Migrar" onClick={() => setConfirm("migrate")} disabled={running} />
          <ActionButton icon={Rocket} label="Redeploy" onClick={() => setConfirm("redeploy")} disabled={running} />
          {running && <span className="text-xs text-gold flex items-center gap-1"><Loader2 className="w-3 h-3 animate-spin" /> ejecutando…</span>}
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          {/* Latency chart */}
          <div className="rounded-xl border border-white/10 p-5">
            <h3 className="text-sm font-medium text-gray-300 mb-4">Latencia health (ms)</h3>
            {latencyData.length === 0 ? (
              <p className="text-xs text-gray-500">Sin datos de health todavía.</p>
            ) : (
              <ResponsiveContainer width="100%" height={200}>
                <LineChart data={latencyData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" />
                  <XAxis dataKey="t" tick={{ fontSize: 10, fill: "#9CA3AF" }} hide />
                  <YAxis tick={{ fontSize: 10, fill: "#9CA3AF" }} />
                  <Tooltip contentStyle={{ background: "#111827", border: "1px solid #ffffff20", borderRadius: 8, fontSize: 12 }} />
                  <Line type="monotone" dataKey="latency" stroke="#3B82F6" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            )}
          </div>

          {/* Metrics / funnel */}
          <div className="rounded-xl border border-white/10 p-5">
            <h3 className="text-sm font-medium text-gray-300 mb-4">Métricas del producto</h3>
            {metrics ? (
              <pre className="text-xs text-gray-400 overflow-auto max-h-[200px] whitespace-pre-wrap">{JSON.stringify(metrics, null, 2)}</pre>
            ) : (
              <p className="text-xs text-gray-500">Sin métricas (el endpoint /analytics del producto no respondió todavía).</p>
            )}
          </div>
        </div>

        {/* Logs */}
        <div className="rounded-xl border border-white/10 p-5 mt-6">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-medium text-gray-300 flex items-center gap-2"><FileText className="w-4 h-4" /> Logs</h3>
            <button onClick={fetchLogs} disabled={logsLoading} className="text-xs px-3 py-1.5 rounded-lg border border-white/10 text-gray-300 hover:bg-white/5">
              {logsLoading ? "Cargando…" : "Obtener logs"}
            </button>
          </div>
          {logs ? (
            <pre className="text-xs text-gray-400 bg-black/30 rounded-lg p-3 overflow-auto max-h-[300px] whitespace-pre-wrap">{logs}</pre>
          ) : (
            <p className="text-xs text-gray-500">Pulsa "Obtener logs" para leer del agente del host.</p>
          )}
        </div>

        {/* Audit history */}
        <div className="rounded-xl border border-white/10 p-5 mt-6">
          <h3 className="text-sm font-medium text-gray-300 mb-3">Historial de acciones (auditoría)</h3>
          {actions.length === 0 ? (
            <p className="text-xs text-gray-500">Sin acciones registradas.</p>
          ) : (
            <table className="w-full text-sm">
              <thead className="text-gray-400 text-xs">
                <tr><th className="text-left py-2">Acción</th><th className="text-left py-2">Estado</th><th className="text-left py-2">Fecha</th><th className="text-left py-2">Salida</th></tr>
              </thead>
              <tbody>
                {actions.map((a) => (
                  <tr key={a.id} className="border-t border-white/5">
                    <td className="py-2 capitalize text-gray-300">{a.action}</td>
                    <td className={`py-2 capitalize ${ACTION_BADGE[a.status] || "text-gray-400"}`}>{a.status}</td>
                    <td className="py-2 text-gray-500">{new Date(a.created_at).toLocaleString()}</td>
                    <td className="py-2 text-gray-500 truncate max-w-[260px]" title={a.output || ""}>{a.output?.split("\n")[0] || "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </main>

      {confirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-black/60" onClick={() => setConfirm(null)} />
          <div className="relative w-full max-w-sm rounded-xl border border-white/10 bg-eko-graphite p-6">
            <div className="flex items-center gap-2 text-gold mb-3"><AlertTriangle className="w-5 h-5" /><h2 className="font-semibold capitalize">{confirm}</h2></div>
            <p className="text-sm text-gray-400 mb-5">
              Vas a ejecutar <b className="text-white capitalize">{confirm}</b> en <b className="text-white">{inst?.client_name}</b>. Esta acción es destructiva y quedará auditada.
            </p>
            <div className="flex gap-3">
              <button onClick={() => setConfirm(null)} className="flex-1 py-2 rounded-lg border border-white/10 text-sm text-gray-300 hover:bg-white/5">Cancelar</button>
              <button onClick={() => runAction(confirm)} className="flex-1 py-2 rounded-lg bg-eko-blue text-white text-sm font-medium">Confirmar</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function ActionButton({ icon: Icon, label, onClick, disabled }: { icon: any; label: string; onClick: () => void; disabled?: boolean }) {
  return (
    <button onClick={onClick} disabled={disabled} className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm border border-white/10 text-gray-300 hover:bg-white/5 disabled:opacity-50">
      <Icon className="w-4 h-4" /> {label}
    </button>
  );
}
