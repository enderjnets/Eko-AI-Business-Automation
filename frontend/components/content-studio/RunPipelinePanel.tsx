"use client";

import { useEffect, useState, useRef, useCallback } from "react";
import {
  Play,
  Loader2,
  CheckCircle,
  XCircle,
  AlertTriangle,
  RefreshCw,
  Terminal,
  FileText,
  Clapperboard,
  Upload,
  Share2,
  ChevronDown,
  ChevronUp,
  Clock,
} from "lucide-react";

interface Brief {
  filename: string;
  business_name: string;
  industry: string;
  city: string;
}

interface HealthStatus {
  status: string;
  message?: string;
}

interface Job {
  job_id: string;
  status: string;
  brief: string;
  stages: Record<string, boolean>;
  started_at: string;
  completed_at?: string;
  error?: string;
}

const PIPELINE_API_URL = "http://100.88.47.99:8002";

const STAGES = [
  { key: "content", label: "Content", description: "Generar guiones", icon: FileText },
  { key: "produce", label: "Produce", description: "Producir videos", icon: Clapperboard },
  { key: "upload", label: "Upload", description: "Subir a cloud", icon: Upload },
  { key: "publish", label: "Publish", description: "Publicar en redes", icon: Share2 },
];

const SERVICE_LABELS: Record<string, string> = {
  buffer: "Buffer",
  elevenlabs: "ElevenLabs TTS",
  huggingface: "Hugging Face",
  minimax: "MiniMax Hailuo",
};

export default function RunPipelinePanel() {
  const [health, setHealth] = useState<Record<string, HealthStatus>>({});
  const [briefs, setBriefs] = useState<Brief[]>([]);
  const [selectedBrief, setSelectedBrief] = useState("");
  const [selectedStages, setSelectedStages] = useState<Record<string, boolean>>({
    content: true,
    produce: false,
    upload: false,
    publish: false,
  });
  const [jobs, setJobs] = useState<Job[]>([]);
  const [activeJobId, setActiveJobId] = useState<string | null>(null);
  const [activeJobLogs, setActiveJobLogs] = useState<string[]>([]);
  const [running, setRunning] = useState(false);
  const [loadingHealth, setLoadingHealth] = useState(true);
  const [loadingBriefs, setLoadingBriefs] = useState(true);
  const [expandedJob, setExpandedJob] = useState<string | null>(null);
  const logsEndRef = useRef<HTMLDivElement>(null);

  const fetchHealth = useCallback(async () => {
    try {
      const res = await fetch(`${PIPELINE_API_URL}/health`);
      const data = await res.json();
      setHealth(data);
    } catch {
      setHealth({});
    } finally {
      setLoadingHealth(false);
    }
  }, []);

  const fetchBriefs = useCallback(async () => {
    try {
      const res = await fetch(`${PIPELINE_API_URL}/briefs`);
      const data = await res.json();
      setBriefs(data.briefs || []);
      if (data.briefs?.length > 0 && !selectedBrief) {
        setSelectedBrief(data.briefs[0].filename);
      }
    } catch {
      setBriefs([]);
    } finally {
      setLoadingBriefs(false);
    }
  }, [selectedBrief]);

  const fetchJobs = useCallback(async () => {
    try {
      const res = await fetch(`${PIPELINE_API_URL}/jobs`);
      const data = await res.json();
      setJobs(data.jobs || []);
    } catch {
      // ignore
    }
  }, []);

  useEffect(() => {
    fetchHealth();
    fetchBriefs();
    fetchJobs();
    const interval = setInterval(() => {
      fetchHealth();
      fetchJobs();
    }, 10000);
    return () => clearInterval(interval);
  }, [fetchHealth, fetchBriefs, fetchJobs]);

  // Poll active job logs
  useEffect(() => {
    if (!activeJobId) return;
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${PIPELINE_API_URL}/jobs/${activeJobId}`);
        const data = await res.json();
        setActiveJobLogs(data.logs || []);
        if (data.status === "completed" || data.status === "failed") {
          setRunning(false);
          fetchJobs();
        }
      } catch {
        // ignore
      }
    }, 2000);
    return () => clearInterval(interval);
  }, [activeJobId, fetchJobs]);

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [activeJobLogs]);

  const handleRun = async () => {
    if (!selectedBrief) return;
    setRunning(true);
    setActiveJobLogs([]);
    try {
      const res = await fetch(`${PIPELINE_API_URL}/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          brief: selectedBrief,
          ...selectedStages,
        }),
      });
      const data = await res.json();
      if (data.job_id) {
        setActiveJobId(data.job_id);
      } else {
        setRunning(false);
      }
    } catch {
      setRunning(false);
    }
  };

  const toggleStage = (key: string) => {
    setSelectedStages((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const statusIcon = (status: string) => {
    switch (status) {
      case "ok":
        return <CheckCircle className="w-4 h-4 text-eko-green" />;
      case "rate_limited":
        return <AlertTriangle className="w-4 h-4 text-yellow-400" />;
      case "error":
        return <XCircle className="w-4 h-4 text-red-400" />;
      default:
        return <XCircle className="w-4 h-4 text-gray-500" />;
    }
  };

  const statusLabel = (status: string) => {
    switch (status) {
      case "ok":
        return "Activo";
      case "rate_limited":
        return "Rate limit";
      case "error":
        return "Error";
      default:
        return "Desconocido";
    }
  };

  return (
    <div className="space-y-6">
      {/* API Health */}
      <div className="rounded-xl border border-white/5 bg-white/[0.02] p-4">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-medium text-gray-400">
            Estado de APIs
          </h3>
          <button
            onClick={fetchHealth}
            className="p-1 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
            title="Refrescar"
          >
            <RefreshCw className="w-3.5 h-3.5" />
          </button>
        </div>
        {loadingHealth ? (
          <div className="flex items-center gap-2 text-sm text-gray-500">
            <Loader2 className="w-4 h-4 animate-spin" />
            Verificando...
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {Object.entries(health).map(([key, value]) => (
              <div
                key={key}
                className="rounded-lg bg-white/5 p-3 flex items-center gap-2"
              >
                {statusIcon(value.status)}
                <div>
                  <p className="text-xs font-medium text-gray-300">
                    {SERVICE_LABELS[key] || key}
                  </p>
                  <p className="text-[10px] text-gray-500">
                    {statusLabel(value.status)}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Run Pipeline */}
      <div className="rounded-xl border border-white/5 bg-white/[0.02] p-4">
        <h3 className="text-sm font-medium text-gray-400 mb-4">
          Ejecutar Pipeline
        </h3>

        {/* Brief selector */}
        <div className="mb-4">
          <label className="text-xs text-gray-500 mb-1.5 block">Brief</label>
          {loadingBriefs ? (
            <div className="flex items-center gap-2 text-sm text-gray-500">
              <Loader2 className="w-4 h-4 animate-spin" />
              Cargando...
            </div>
          ) : briefs.length === 0 ? (
            <p className="text-sm text-gray-500">No hay briefs disponibles.</p>
          ) : (
            <select
              value={selectedBrief}
              onChange={(e) => setSelectedBrief(e.target.value)}
              className="w-full rounded-lg bg-white/5 border border-white/10 px-3 py-2 text-sm text-gray-300 focus:outline-none focus:border-pink-400/50"
            >
              {briefs.map((b) => (
                <option key={b.filename} value={b.filename}>
                  {b.business_name} ({b.city}) — {b.industry}
                </option>
              ))}
            </select>
          )}
        </div>

        {/* Stage toggles */}
        <div className="mb-4">
          <label className="text-xs text-gray-500 mb-1.5 block">Etapas</label>
          <div className="flex flex-wrap gap-2">
            {STAGES.map((stage) => {
              const Icon = stage.icon;
              const active = selectedStages[stage.key];
              return (
                <button
                  key={stage.key}
                  onClick={() => toggleStage(stage.key)}
                  disabled={running}
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-medium transition-colors border ${
                    active
                      ? "bg-pink-500/10 text-pink-400 border-pink-500/30"
                      : "bg-white/5 text-gray-400 border-white/5 hover:bg-white/10"
                  } ${running ? "opacity-50 cursor-not-allowed" : ""}`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <div className="text-left">
                    <div>{stage.label}</div>
                    <div className="text-[10px] text-gray-500">
                      {stage.description}
                    </div>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Run button */}
        <div className="flex items-center gap-3">
          <button
            onClick={handleRun}
            disabled={running || !selectedBrief}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              running || !selectedBrief
                ? "bg-white/5 text-gray-500 cursor-not-allowed"
                : "bg-pink-500/20 text-pink-400 hover:bg-pink-500/30 border border-pink-500/30"
            }`}
          >
            {running ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Ejecutando...
              </>
            ) : (
              <>
                <Play className="w-4 h-4" />
                Ejecutar pipeline
              </>
            )}
          </button>
          {activeJobId && running && (
            <span className="text-xs text-gray-500">
              Job: {activeJobId.slice(0, 8)}...
            </span>
          )}
        </div>

        {/* Live logs */}
        {activeJobId && (
          <div className="mt-4">
            <div className="flex items-center gap-2 mb-2">
              <Terminal className="w-3.5 h-3.5 text-gray-400" />
              <span className="text-xs text-gray-400">Logs en tiempo real</span>
              {running && (
                <Loader2 className="w-3 h-3 animate-spin text-eko-blue" />
              )}
            </div>
            <div className="rounded-lg bg-black/40 border border-white/5 p-3 font-mono text-[11px] text-gray-300 h-64 overflow-y-auto">
              {activeJobLogs.length === 0 ? (
                <span className="text-gray-600">Esperando inicio...</span>
              ) : (
                activeJobLogs.map((line, i) => (
                  <div key={i} className="leading-relaxed">
                    {line}
                  </div>
                ))
              )}
              <div ref={logsEndRef} />
            </div>
          </div>
        )}
      </div>

      {/* Job History */}
      <div className="rounded-xl border border-white/5 bg-white/[0.02] p-4">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-medium text-gray-400">
            Historial de ejecuciones
          </h3>
          <button
            onClick={fetchJobs}
            className="p-1 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" />
          </button>
        </div>

        {jobs.length === 0 ? (
          <p className="text-sm text-gray-500">Sin ejecuciones recientes.</p>
        ) : (
          <div className="space-y-2">
            {jobs.map((job) => {
              const isExpanded = expandedJob === job.job_id;
              const isActive = activeJobId === job.job_id;
              const statusColor =
                job.status === "completed"
                  ? "text-eko-green"
                  : job.status === "failed"
                  ? "text-red-400"
                  : job.status === "running"
                  ? "text-eko-blue"
                  : "text-yellow-400";

              return (
                <div
                  key={job.job_id}
                  className={`rounded-lg border p-3 transition-colors ${
                    isActive
                      ? "bg-white/[0.04] border-pink-400/20"
                      : "bg-white/5 border-white/5"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className={`text-xs font-medium ${statusColor}`}>
                        {job.status === "completed"
                          ? "✓ Completado"
                          : job.status === "failed"
                          ? "✗ Fallido"
                          : job.status === "running"
                          ? "⟳ En ejecución"
                          : "⏳ Pendiente"}
                      </span>
                      <span className="text-[10px] text-gray-500">
                        {job.brief}
                      </span>
                    </div>
                    <div className="flex items-center gap-1">
                      <span className="text-[10px] text-gray-500">
                        {new Date(job.started_at).toLocaleString("es-CO", {
                          month: "short",
                          day: "numeric",
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                      </span>
                      <button
                        onClick={() =>
                          setExpandedJob(isExpanded ? null : job.job_id)
                        }
                        className="p-1 rounded text-gray-400 hover:text-white"
                      >
                        {isExpanded ? (
                          <ChevronUp className="w-3 h-3" />
                        ) : (
                          <ChevronDown className="w-3 h-3" />
                        )}
                      </button>
                    </div>
                  </div>

                  {isExpanded && (
                    <div className="mt-2 pt-2 border-t border-white/5">
                      <div className="text-[10px] text-gray-500 mb-1">
                        ID: {job.job_id}
                      </div>
                      <div className="text-[10px] text-gray-500 mb-2">
                        Etapas:{" "}
                        {Object.entries(job.stages || {})
                          .filter(([, v]) => v)
                          .map(([k]) => k)
                          .join(", ") || "content"}
                      </div>
                      {job.error && (
                        <div className="text-[10px] text-red-400 mb-2">
                          Error: {job.error}
                        </div>
                      )}
                      <JobLogs jobId={job.job_id} />
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

function JobLogs({ jobId }: { jobId: string }) {
  const [logs, setLogs] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${PIPELINE_API_URL}/jobs/${jobId}`)
      .then((r) => r.json())
      .then((data) => {
        setLogs(data.logs || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [jobId]);

  if (loading) {
    return (
      <div className="flex items-center gap-2 text-[10px] text-gray-500">
        <Loader2 className="w-3 h-3 animate-spin" />
        Cargando logs...
      </div>
    );
  }

  return (
    <div className="rounded bg-black/30 p-2 font-mono text-[10px] text-gray-400 max-h-40 overflow-y-auto">
      {logs.length === 0 ? (
        <span className="text-gray-600">Sin logs.</span>
      ) : (
        logs.slice(-50).map((line, i) => (
          <div key={i} className="leading-relaxed">
            {line}
          </div>
        ))
      )}
    </div>
  );
}
