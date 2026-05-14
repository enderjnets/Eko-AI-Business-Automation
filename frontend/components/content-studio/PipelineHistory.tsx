"use client";

import { useEffect, useState } from "react";
import { Play, CheckCircle, XCircle, Clock, Loader2 } from "lucide-react";

interface Pipeline {
  filename: string;
  started_at: string;
  business_name: string;
  stages: Record<string, { status: string }>;
  paperclip_issue_id?: string;
}

export default function PipelineHistory() {
  const [pipelines, setPipelines] = useState<Pipeline[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/content-api/pipelines")
      .then((r) => r.json())
      .then((data) => {
        setPipelines(data.pipelines || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-eko-blue" />
      </div>
    );
  }

  const statusIcon = (status?: string) => {
    if (status === "completed")
      return <CheckCircle className="w-4 h-4 text-eko-green" />;
    if (status === "failed")
      return <XCircle className="w-4 h-4 text-red-500" />;
    return <Clock className="w-4 h-4 text-gray-500" />;
  };

  return (
    <div className="rounded-xl border border-white/5 bg-white/[0.02] overflow-hidden">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-white/5 text-left text-gray-500">
            <th className="px-4 py-3 font-medium">Fecha</th>
            <th className="px-4 py-3 font-medium">Negocio</th>
            <th className="px-4 py-3 font-medium">Content</th>
            <th className="px-4 py-3 font-medium">Produce</th>
            <th className="px-4 py-3 font-medium">Upload</th>
            <th className="px-4 py-3 font-medium">Publish</th>
            <th className="px-4 py-3 font-medium">Paperclip</th>
          </tr>
        </thead>
        <tbody>
          {pipelines.map((p) => (
            <tr
              key={p.filename}
              className="border-b border-white/5 hover:bg-white/[0.02] transition-colors"
            >
              <td className="px-4 py-3 text-gray-400">
                {new Date(p.started_at).toLocaleDateString("es-CO")}
              </td>
              <td className="px-4 py-3 font-medium">{p.business_name}</td>
              {["content", "produce", "upload", "publish"].map((stage) => (
                <td key={stage} className="px-4 py-3">
                  <div className="flex items-center gap-1.5">
                    {statusIcon(p.stages?.[stage]?.status)}
                    <span className="text-gray-400 capitalize">{p.stages?.[stage]?.status || "—"}</span>
                  </div>
                </td>
              ))}
              <td className="px-4 py-3 text-gray-500">
                {p.paperclip_issue_id ? (
                  <span className="font-mono text-xs">{p.paperclip_issue_id.slice(0, 8)}...</span>
                ) : (
                  "—"
                )}
              </td>
            </tr>
          ))}
          {pipelines.length === 0 && (
            <tr>
              <td colSpan={7} className="px-4 py-8 text-center text-gray-500">
                No hay pipelines ejecutados aún.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
