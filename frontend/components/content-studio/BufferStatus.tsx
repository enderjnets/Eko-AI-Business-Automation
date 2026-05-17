"use client";

import { useEffect, useState } from "react";
import {
  Loader2,
  RefreshCw,
  CheckCircle,
  Clock,
  Send,
  AlertTriangle,
  Wifi,
  WifiOff,
  BarChart3,
  ChevronDown,
  ChevronUp,
  ImageOff,
  Eye,
  EyeOff,
} from "lucide-react";

interface Post {
  id: string;
  text: string;
  status: string;
  dueAt?: string;
  sentAt?: string;
  createdAt: string;
  channelId: string;
  channelService: string;
  channel?: { name: string };
  assets?: { source?: string; thumbnail?: string; mimeType?: string }[];
  externalLink?: string;
  error?: { message?: string };
}

interface Channel {
  id: string;
  name: string;
  service: string;
  isDisconnected: boolean;
}

interface ChannelStats {
  total: number;
  sent: number;
  scheduled: number;
  sending: number;
  error: number;
  draft: number;
}

const serviceColors: Record<string, string> = {
  tiktok: "text-white",
  instagram: "text-pink-400",
  facebook: "text-blue-400",
};

const STATUS_CONFIG: Record<string, { color: string; icon: any; label: string }> = {
  sent: { color: "text-eko-green", icon: CheckCircle, label: "Publicado" },
  scheduled: { color: "text-yellow-400", icon: Clock, label: "Programado" },
  sending: { color: "text-eko-blue", icon: Send, label: "Enviando" },
  error: { color: "text-red-400", icon: AlertTriangle, label: "Error" },
  draft: { color: "text-gray-400", icon: Clock, label: "Borrador" },
};

export default function BufferStatus() {
  const [channels, setChannels] = useState<Channel[]>([]);
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [expandedChannel, setExpandedChannel] = useState<string | null>(null);
  const [showErrors, setShowErrors] = useState(false);

  const load = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/content-api/buffer-posts");
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      setChannels(data.channels || []);
      setPosts(data.posts || []);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  // Stats per channel
  const getStats = (channelId: string): ChannelStats => {
    const channelPosts = posts.filter((p) => p.channelId === channelId);
    return {
      total: channelPosts.length,
      sent: channelPosts.filter((p) => p.status === "sent").length,
      scheduled: channelPosts.filter((p) => p.status === "scheduled").length,
      sending: channelPosts.filter((p) => p.status === "sending").length,
      error: channelPosts.filter((p) => p.status === "error").length,
      draft: channelPosts.filter((p) => p.status === "draft").length,
    };
  };

  const totalErrors = posts.filter((p) => p.status === "error").length;

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-eko-blue" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-xl border border-red-500/20 bg-red-500/5 p-4 text-red-400 text-sm">
        {error}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Global stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { label: "Canales", value: channels.length, icon: BarChart3, color: "text-gray-400" },
          { label: "Posts activos", value: posts.filter((p) => p.status !== "error").length, icon: CheckCircle, color: "text-eko-green" },
          { label: "Programados", value: posts.filter((p) => p.status === "scheduled").length, icon: Clock, color: "text-yellow-400" },
          { label: "Errores", value: totalErrors, icon: AlertTriangle, color: "text-red-400" },
        ].map((s) => (
          <div key={s.label} className="rounded-xl border border-white/5 bg-white/[0.02] p-3">
            <div className="flex items-center gap-2 mb-1">
              <s.icon className={`w-4 h-4 ${s.color}`} />
              <span className="text-xs text-gray-500">{s.label}</span>
            </div>
            <div className="text-xl font-bold">{s.value}</div>
          </div>
        ))}
      </div>

      {/* Controls */}
      <div className="flex items-center gap-2">
        <button
          onClick={() => setShowErrors(!showErrors)}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
            showErrors
              ? "bg-red-500/10 text-red-400 border border-red-500/20"
              : "bg-white/5 text-gray-400 border border-white/5 hover:bg-white/10"
          }`}
        >
          {showErrors ? <Eye className="w-3.5 h-3.5" /> : <EyeOff className="w-3.5 h-3.5" />}
          Mostrar errores ({totalErrors})
        </button>
        <button
          onClick={load}
          className="ml-auto p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
          title="Refrescar"
        >
          <RefreshCw className="w-4 h-4" />
        </button>
      </div>

      {/* Channel list */}
      <div className="space-y-2">
        {channels.map((ch) => {
          const stats = getStats(ch.id);
          const isExpanded = expandedChannel === ch.id;
          const channelPosts = posts
            .filter((p) => p.channelId === ch.id)
            .filter((p) => showErrors || p.status !== "error")
            .slice(0, 50);

          return (
            <div key={ch.id} className="rounded-xl border border-white/5 bg-white/[0.02] overflow-hidden">
              {/* Channel header */}
              <button
                onClick={() => setExpandedChannel(isExpanded ? null : ch.id)}
                className="w-full flex items-center justify-between p-4 hover:bg-white/[0.02] transition-colors"
              >
                <div className="flex items-center gap-3">
                  {ch.isDisconnected ? (
                    <WifiOff className="w-4 h-4 text-red-400" />
                  ) : (
                    <Wifi className={`w-4 h-4 ${serviceColors[ch.service] || "text-gray-400"}`} />
                  )}
                  <div className="text-left">
                    <div className="text-sm font-medium">{ch.name}</div>
                    <div className="text-xs text-gray-500 capitalize">{ch.service}</div>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  {/* Mini stats */}
                  <div className="hidden sm:flex items-center gap-2">
                    {stats.error > 0 && (
                      <span className="text-xs text-red-400">
                        {stats.error} error{stats.error > 1 ? "es" : ""}
                      </span>
                    )}
                    {stats.scheduled > 0 && (
                      <span className="text-xs text-yellow-400">
                        {stats.scheduled} prog.
                      </span>
                    )}
                    {stats.sent > 0 && (
                      <span className="text-xs text-eko-green">
                        {stats.sent} pub.
                      </span>
                    )}
                  </div>
                  {isExpanded ? (
                    <ChevronUp className="w-4 h-4 text-gray-500" />
                  ) : (
                    <ChevronDown className="w-4 h-4 text-gray-500" />
                  )}
                </div>
              </button>

              {/* Channel posts */}
              {isExpanded && (
                <div className="border-t border-white/5 p-4 space-y-2 max-h-96 overflow-y-auto">
                  {channelPosts.length === 0 ? (
                    <p className="text-sm text-gray-500">Sin posts recientes.</p>
                  ) : (
                    channelPosts.map((post) => {
                      const config = STATUS_CONFIG[post.status] || STATUS_CONFIG.draft;
                      const StatusIcon = config.icon;
                      const thumbnail = post.assets?.[0]?.thumbnail;
                      const proxyUrl = thumbnail
                        ? `/content-api/proxy-image?url=${encodeURIComponent(thumbnail)}`
                        : null;

                      return (
                        <div
                          key={post.id}
                          className={`flex gap-3 rounded-lg p-3 ${
                            post.status === "error"
                              ? "bg-red-500/5 border border-red-500/10"
                              : "bg-white/5"
                          }`}
                        >
                          {proxyUrl ? (
                            <img
                              src={proxyUrl}
                              alt=""
                              className="w-12 h-12 rounded-lg object-cover flex-shrink-0"
                              onError={(e) => {
                                (e.target as HTMLImageElement).style.display = "none";
                              }}
                            />
                          ) : (
                            <div className="w-12 h-12 rounded-lg bg-white/5 flex items-center justify-center flex-shrink-0">
                              <ImageOff className="w-5 h-5 text-gray-600" />
                            </div>
                          )}
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 mb-1">
                              <StatusIcon className={`w-3 h-3 ${config.color}`} />
                              <span className="text-[10px] text-gray-400">{config.label}</span>
                              {post.dueAt && (
                                <span className="text-[10px] text-gray-500">
                                  {new Date(post.dueAt).toLocaleString("es-CO", {
                                    month: "short",
                                    day: "numeric",
                                    hour: "2-digit",
                                    minute: "2-digit",
                                  })}
                                </span>
                              )}
                            </div>
                            <p className="text-sm line-clamp-2">{post.text}</p>
                            {post.error?.message && (
                              <p className="text-[10px] text-red-400/80 mt-1 line-clamp-2">
                                {post.error.message}
                              </p>
                            )}
                          </div>
                        </div>
                      );
                    })
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
