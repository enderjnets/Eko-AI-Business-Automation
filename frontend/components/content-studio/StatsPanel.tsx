"use client";

import { useEffect, useState } from "react";
import { Film, Clock, HardDrive, CheckCircle, FileText } from "lucide-react";

interface Stats {
  total_pipelines: number;
  total_videos: number;
  total_duration_seconds: number;
  total_size_mb: number;
  published_videos: number;
  total_briefs: number;
  by_platform: Record<string, number>;
}

export default function StatsPanel() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/content-api/stats")
      .then((r) => r.json())
      .then((data) => {
        setStats(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="w-6 h-6 border-2 border-eko-blue border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!stats) return null;

  const cards = [
    {
      label: "Videos producidos",
      value: stats.total_videos,
      icon: Film,
      color: "text-eko-blue",
    },
    {
      label: "Duración total",
      value: `${Math.floor(stats.total_duration_seconds / 60)}m ${stats.total_duration_seconds % 60}s`,
      icon: Clock,
      color: "text-eko-green",
    },
    {
      label: "Espacio usado",
      value: `${stats.total_size_mb} MB`,
      icon: HardDrive,
      color: "text-gold",
    },
    {
      label: "Publicados",
      value: stats.published_videos,
      icon: CheckCircle,
      color: "text-emerald-400",
    },
    {
      label: "Briefs",
      value: stats.total_briefs,
      icon: FileText,
      color: "text-purple-400",
    },
  ];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        {cards.map((c) => (
          <div
            key={c.label}
            className="rounded-xl border border-white/5 bg-white/[0.02] p-4"
          >
            <div className={`${c.color} mb-2`}>
              <c.icon className="w-5 h-5" />
            </div>
            <p className="text-2xl font-bold">{c.value}</p>
            <p className="text-xs text-gray-500 mt-1">{c.label}</p>
          </div>
        ))}
      </div>

      {Object.keys(stats.by_platform).length > 0 && (
        <div className="rounded-xl border border-white/5 bg-white/[0.02] p-4">
          <h3 className="text-sm font-medium text-gray-400 mb-3">
            Publicaciones por plataforma
          </h3>
          <div className="flex gap-4">
            {Object.entries(stats.by_platform).map(([platform, count]) => (
              <div
                key={platform}
                className="px-3 py-1.5 rounded-lg bg-white/5 text-sm"
              >
                <span className="capitalize text-gray-400">{platform}:</span>{" "}
                <span className="font-semibold text-white">{count}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
