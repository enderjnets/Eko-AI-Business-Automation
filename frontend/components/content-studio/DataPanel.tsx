"use client";

import { useEffect, useState } from "react";
import { Loader2 } from "lucide-react";

interface Brief {
  filename: string;
  business_name: string;
  industry: string;
  city: string;
}

interface ScriptItem {
  title: string;
  type: string;
  tags: string[];
  video_duration?: number;
  video_size_mb?: number;
}

export default function DataPanel() {
  const [briefs, setBriefs] = useState<Brief[]>([]);
  const [scripts, setScripts] = useState<ScriptItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch("/content-api/briefs").then((r) => r.json()),
      fetch("/content-api/scripts").then((r) => r.json()),
    ])
      .then(([briefsData, scriptsData]) => {
        setBriefs(briefsData.briefs || []);
        setScripts(scriptsData.scripts || []);
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

  return (
    <div className="space-y-6">
      {/* Briefs */}
      <div>
        <h3 className="text-sm font-medium text-gray-400 mb-3">Briefs</h3>
        <div className="rounded-xl border border-white/5 bg-white/[0.02] overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-white/5 text-left text-gray-500">
                <th className="px-4 py-3 font-medium">Negocio</th>
                <th className="px-4 py-3 font-medium">Industria</th>
                <th className="px-4 py-3 font-medium">Ciudad</th>
              </tr>
            </thead>
            <tbody>
              {briefs.map((b) => (
                <tr
                  key={b.filename}
                  className="border-b border-white/5 hover:bg-white/[0.02] transition-colors"
                >
                  <td className="px-4 py-3 font-medium">{b.business_name}</td>
                  <td className="px-4 py-3 text-gray-400 capitalize">{b.industry}</td>
                  <td className="px-4 py-3 text-gray-400">{b.city}</td>
                </tr>
              ))}
              {briefs.length === 0 && (
                <tr>
                  <td colSpan={3} className="px-4 py-8 text-center text-gray-500">
                    No hay briefs.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Scripts */}
      <div>
        <h3 className="text-sm font-medium text-gray-400 mb-3">
          Scripts del último pipeline
        </h3>
        <div className="space-y-3">
          {scripts.map((s, i) => (
            <div
              key={i}
              className="rounded-xl border border-white/5 bg-white/[0.02] p-4"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs px-2 py-0.5 rounded bg-white/10 text-gray-400 uppercase">
                  {s.type}
                </span>
                {s.video_duration && (
                  <span className="text-xs text-gray-500">
                    {Math.round(s.video_duration)}s · {s.video_size_mb}MB
                  </span>
                )}
              </div>
              <p className="font-medium">{s.title}</p>
              <div className="flex flex-wrap gap-1 mt-2">
                {s.tags?.slice(0, 6).map((t) => (
                  <span
                    key={t}
                    className="text-[10px] px-1.5 py-0.5 rounded bg-white/5 text-gray-500"
                  >
                    #{t}
                  </span>
                ))}
              </div>
            </div>
          ))}
          {scripts.length === 0 && (
            <p className="text-center text-gray-500 py-8">No hay scripts.</p>
          )}
        </div>
      </div>
    </div>
  );
}
