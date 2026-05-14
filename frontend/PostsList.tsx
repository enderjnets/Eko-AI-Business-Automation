"use client";

import { useEffect, useState } from "react";
import { Loader2, Trash2, ExternalLink, Pencil, RefreshCw, Send, Clock, AlertTriangle, CheckCircle } from "lucide-react";

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

const STATUS_CONFIG: Record<string, { label: string; color: string; icon: any }> = {
  sent: { label: "Publicado", color: "bg-eko-green/10 text-eko-green border-eko-green/20", icon: CheckCircle },
  scheduled: { label: "Programado", color: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20", icon: Clock },
  sending: { label: "Enviando", color: "bg-eko-blue/10 text-eko-blue border-eko-blue/20", icon: Send },
  error: { label: "Error", color: "bg-red-500/10 text-red-400 border-red-500/20", icon: AlertTriangle },
  draft: { label: "Borrador", color: "bg-gray-500/10 text-gray-400 border-gray-500/20", icon: Pencil },
  needs_approval: { label: "Pendiente", color: "bg-purple-500/10 text-purple-400 border-purple-500/20", icon: Clock },
};

export default function PostsList() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
  const [error, setError] = useState("");

  const loadPosts = async () => {
    setLoading(true);
    setError("");
    try {
      const url = filter === "all" ? "/content-api/posts" : `/content-api/posts?status=${filter}`;
      const res = await fetch(url);
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      setPosts(data.posts || []);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPosts();
  }, [filter]);

  const handleDelete = async (id: string) => {
    if (!confirm("Seguro que quieres borrar este post?")) return;
    try {
      const res = await fetch(`/content-api/posts/${id}/delete`, { method: "POST" });
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      setPosts((prev) => prev.filter((p) => p.id !== id));
    } catch (e: any) {
      alert("Error borrando: " + e.message);
    }
  };

  const handleEdit = async (id: string, currentText: string) => {
    const newText = prompt("Nuevo texto del post:", currentText);
    if (!newText || newText === currentText) return;
    try {
      const res = await fetch(`/content-api/posts/${id}/edit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: newText }),
      });
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      setPosts((prev) => prev.map((p) => (p.id === id ? { ...p, text: newText } : p)));
    } catch (e: any) {
      alert("Error editando: " + e.message);
    }
  };

  const statusConfig = (status: string) =>
    STATUS_CONFIG[status] || { label: status, color: "bg-gray-500/10 text-gray-400", icon: Clock };

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-2">
        {[
          { value: "all", label: "Todos" },
          { value: "sent", label: "Publicados" },
          { value: "scheduled", label: "Programados" },
          { value: "sending", label: "Enviando" },
          { value: "error", label: "Errores" },
          { value: "draft", label: "Borradores" },
          { value: "needs_approval", label: "Pendientes" },
        ].map((f) => (
          <button
            key={f.value}
            onClick={() => setFilter(f.value)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              filter === f.value
                ? "bg-pink-500/20 text-pink-400 border border-pink-500/30"
                : "bg-white/5 text-gray-400 border border-white/5 hover:bg-white/10"
            }`}
          >
            {f.label}
          </button>
        ))}
        <button
          onClick={loadPosts}
          className="ml-auto p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
          title="Refrescar"
        >
          <RefreshCw className="w-4 h-4" />
        </button>
      </div>

      {loading && (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-6 h-6 animate-spin text-eko-blue" />
        </div>
      )}

      {error && (
        <div className="rounded-xl border border-red-500/20 bg-red-500/5 p-4 text-red-400 text-sm">
          {error}
        </div>
      )}

      {!loading && !error && posts.length === 0 && (
        <div className="text-center py-12 text-gray-500">No hay posts con este filtro.</div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {posts.map((post) => {
          const status = statusConfig(post.status);
          const StatusIcon = status.icon;
          const thumbnail = post.assets?.[0]?.thumbnail || post.assets?.[0]?.source;

          return (
            <div key={post.id} className="rounded-xl border border-white/5 bg-white/[0.02] overflow-hidden hover:border-white/10 transition-colors">
              {thumbnail ? (
                <div className="aspect-video bg-black/30 relative">
                  <img src={thumbnail} alt="" className="w-full h-full object-cover" onError={(e) => { (e.target as HTMLImageElement).style.display = "none"; }} />
                </div>
              ) : (
                <div className="aspect-video bg-white/5 flex items-center justify-center">
                  <span className="text-xs text-gray-600">Sin preview</span>
                </div>
              )}

              <div className="p-4">
                <div className="flex items-center gap-2 mb-2">
                  <span className={`text-[10px] px-2 py-0.5 rounded-full border ${status.color}`}>
                    <StatusIcon className="w-3 h-3 inline mr-1" />
                    {status.label}
                  </span>
                  <span className="text-[10px] text-gray-500 capitalize">{post.channelService}</span>
                </div>

                <p className="text-sm line-clamp-3 mb-2">{post.text}</p>

                <div className="flex items-center gap-1 text-[10px] text-gray-500 mb-3">
                  {post.dueAt && post.status === "scheduled" && <span>Programado: {new Date(post.dueAt).toLocaleString("es-CO", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" })}</span>}
                  {post.sentAt && <span>Publicado: {new Date(post.sentAt).toLocaleString("es-CO", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" })}</span>}
                  {!post.dueAt && !post.sentAt && <span>Creado: {new Date(post.createdAt).toLocaleDateString("es-CO")}</span>}
                </div>

                {post.error?.message && (
                  <div className="text-[10px] text-red-400 mb-2 line-clamp-2">{post.error.message}</div>
                )}

                <div className="flex items-center gap-1">
                  <button
                    onClick={() => handleEdit(post.id, post.text)}
                    className="p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
                    title="Editar texto"
                  >
                    <Pencil className="w-3.5 h-3.5" />
                  </button>
                  {post.externalLink && (
                    <a
                      href={post.externalLink}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
                      title="Ver en plataforma"
                    >
                      <ExternalLink className="w-3.5 h-3.5" />
                    </a>
                  )}
                  <button
                    onClick={() => handleDelete(post.id)}
                    className="p-1.5 rounded-lg text-gray-400 hover:text-red-400 hover:bg-red-500/10 transition-colors ml-auto"
                    title="Borrar"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
