"use client";

import { useEffect, useState } from "react";
import { Loader2, CheckCircle, XCircle, Clock, Send, AlertTriangle } from "lucide-react";

interface Channel {
  id: string;
  name: string;
  service: string;
  isDisconnected: boolean;
}

interface Post {
  id: string;
  text: string;
  status: string;
  dueAt?: string;
  sentAt?: string;
  channelId: string;
}

export default function BufferStatus() {
  const [channels, setChannels] = useState<Channel[]>([]);
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/content-api/buffer-posts")
      .then((r) => r.json())
      .then((data) => {
        if (data.error) {
          setError(data.error);
        } else {
          setChannels(data.channels || []);
          setPosts(data.posts || []);
        }
        setLoading(false);
      })
      .catch((e) => {
        setError(e.message);
        setLoading(false);
      });
  }, []);

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

  const serviceColors: Record<string, string> = {
    tiktok: "text-black bg-white border-white/20",
    instagram: "text-pink-400 bg-pink-500/10 border-pink-500/20",
    facebook: "text-blue-400 bg-blue-500/10 border-blue-500/20",
  };

  const statusIcon = (status: string) => {
    switch (status) {
      case "sent":
        return <CheckCircle className="w-4 h-4 text-eko-green" />;
      case "sending":
        return <Send className="w-4 h-4 text-eko-blue animate-pulse" />;
      case "scheduled":
        return <Clock className="w-4 h-4 text-yellow-400" />;
      case "error":
        return <AlertTriangle className="w-4 h-4 text-red-500" />;
      default:
        return <Clock className="w-4 h-4 text-gray-500" />;
    }
  };

  const statusLabel = (status: string) => {
    switch (status) {
      case "sent":
        return "Publicado";
      case "sending":
        return "Enviando...";
      case "scheduled":
        return "Programado";
      case "error":
        return "Error";
      default:
        return status;
    }
  };

  const postsByChannel = (channelId: string) =>
    posts.filter((p) => p.channelId === channelId);

  return (
    <div className="space-y-4">
      {channels.map((ch) => {
        const chPosts = postsByChannel(ch.id);
        return (
          <div
            key={ch.id}
            className={`rounded-xl border p-4 ${
              serviceColors[ch.service] ||
              "text-gray-400 bg-white/[0.02] border-white/5"
            }`}
          >
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <span className="font-semibold capitalize">{ch.service}</span>
                <span className="text-sm text-gray-500">{ch.name}</span>
              </div>
              {ch.isDisconnected ? (
                <XCircle className="w-4 h-4 text-red-500" />
              ) : (
                <CheckCircle className="w-4 h-4 text-eko-green" />
              )}
            </div>

            {chPosts.length === 0 ? (
              <p className="text-sm text-gray-500">Sin posts</p>
            ) : (
              <div className="space-y-2">
                {chPosts.map((p) => (
                  <div
                    key={p.id}
                    className="flex items-center gap-3 rounded-lg bg-white/5 p-2.5"
                  >
                    {statusIcon(p.status)}
                    <div className="flex-1 min-w-0">
                      <p className="text-sm truncate">{p.text || "(sin texto)"}</p>
                      <div className="flex items-center gap-2 mt-0.5">
                        <span className="text-[10px] text-gray-500">
                          {statusLabel(p.status)}
                        </span>
                        {p.dueAt && p.status === "scheduled" && (
                          <span className="text-[10px] text-gray-500">
                            {new Date(p.dueAt).toLocaleString("es-CO", {
                              month: "short",
                              day: "numeric",
                              hour: "2-digit",
                              minute: "2-digit",
                            })}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
