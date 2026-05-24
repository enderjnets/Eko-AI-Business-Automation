"use client";

import { useCallback, useMemo, useState } from "react";
import {
  Loader2,
  Trash2,
  ExternalLink,
  Pencil,
  RefreshCw,
  Send,
  Clock,
  AlertTriangle,
  CheckCircle,
  ImageOff,
  Play,
  Sparkles,
} from "lucide-react";
import VideoModal from "./VideoModal";
import RateLimitBanner from "./RateLimitBanner";
import {
  useBufferData,
  patchBufferPost,
  type BufferPost,
} from "@/hooks/useBufferData";

const STATUS_CONFIG: Record<
  string,
  { label: string; color: string; icon: any }
> = {
  sent: {
    label: "Publicado",
    color: "bg-eko-green/10 text-eko-green border-eko-green/20",
    icon: CheckCircle,
  },
  scheduled: {
    label: "Programado",
    color: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20",
    icon: Clock,
  },
  sending: {
    label: "Enviando",
    color: "bg-eko-blue/10 text-eko-blue border-eko-blue/20",
    icon: Send,
  },
  error: {
    label: "Error",
    color: "bg-red-500/10 text-red-400 border-red-500/20",
    icon: AlertTriangle,
  },
  draft: {
    label: "Borrador",
    color: "bg-gray-500/10 text-gray-400 border-gray-500/20",
    icon: Pencil,
  },
  needs_approval: {
    label: "Pendiente",
    color: "bg-purple-500/10 text-purple-400 border-purple-500/20",
    icon: Clock,
  },
};

export default function PostsList() {
  const { data, loading, refresh } = useBufferData();
  const [filter, setFilter] = useState("all");
  const [modalOpen, setModalOpen] = useState(false);
  const [modalVideoUrl, setModalVideoUrl] = useState("");
  const [modalProxyUrl, setModalProxyUrl] = useState("");
  const [modalTitle, setModalTitle] = useState("");
  const [failedImgIds, setFailedImgIds] = useState<Set<string>>(new Set());
  const [cleaning, setCleaning] = useState(false);

  const markImgFailed = useCallback((postId: string) => {
    setFailedImgIds((prev) => {
      if (prev.has(postId)) return prev;
      const next = new Set(prev);
      next.add(postId);
      return next;
    });
  }, []);

  const allPosts = data?.posts || [];
  const posts = useMemo(
    () =>
      filter === "all"
        ? allPosts
        : allPosts.filter((p) => p.status === filter),
    [allPosts, filter]
  );

  // A post is considered "expired" for cleanup purposes when:
  //   - Buffer marked it status=error (publish failed because source was gone)
  //   - OR its thumbnail URL is set but the <img> failed to load (catbox-style
  //     temp file already deleted)
  const expiredIds = useMemo(() => {
    return allPosts
      .filter((p) => {
        if (p.status === "error") return true;
        const thumb = p.assets?.[0]?.thumbnail;
        return !!thumb && failedImgIds.has(p.id);
      })
      .map((p) => p.id);
  }, [allPosts, failedImgIds]);

  const isExpiredPost = useCallback(
    (post: BufferPost): boolean => {
      if (post.status === "error") return true;
      const thumb = post.assets?.[0]?.thumbnail;
      return !!thumb && failedImgIds.has(post.id);
    },
    [failedImgIds]
  );

  const handleDelete = async (id: string) => {
    if (!confirm("¿Seguro que quieres borrar este post?")) return;
    try {
      const res = await fetch(`/content-api/posts/${id}/delete`, {
        method: "POST",
      });
      const r = await res.json();
      if (r.error) throw new Error(r.error);
      patchBufferPost(id, null);
    } catch (e: any) {
      alert("Error borrando: " + e.message);
    }
  };

  const handleCleanExpired = async () => {
    const ids = expiredIds;
    if (ids.length === 0) return;
    const confirmed = confirm(
      `¿Borrar ${ids.length} post${ids.length === 1 ? "" : "s"} con media expirada de Buffer? Esta acción no se puede deshacer.`
    );
    if (!confirmed) return;
    setCleaning(true);
    try {
      const res = await fetch("/content-api/posts/bulk-delete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ids }),
      });
      const r = await res.json();
      if (!res.ok) throw new Error(r.error || `HTTP ${res.status}`);
      const deleted: string[] = r.deleted || [];
      for (const id of deleted) {
        patchBufferPost(id, null);
      }
      // Drop now-stale failed-img entries
      setFailedImgIds((prev) => {
        const next = new Set(prev);
        for (const id of deleted) next.delete(id);
        return next;
      });
      // Re-fetch authoritative snapshot in the background
      refresh().catch(() => {});
      const failedCount = (r.failed || []).length;
      const total = r.total ?? ids.length;
      if (r.rate_limited) {
        alert(
          `Limpieza parcial: ${deleted.length}/${total} borrados. Buffer está rate-limitado — esperá unos minutos y reintentá para los ${failedCount} restantes.`
        );
      } else if (failedCount > 0) {
        alert(
          `${deleted.length}/${total} borrados. ${failedCount} fallaron — revisar consola para detalles.`
        );
        // eslint-disable-next-line no-console
        console.warn("bulk-delete failures", r.failed);
      }
    } catch (e: any) {
      alert("Error limpiando expirados: " + (e.message || "desconocido"));
    } finally {
      setCleaning(false);
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
      const r = await res.json();
      if (r.error) throw new Error(r.error);
      patchBufferPost(id, { text: newText });
    } catch (e: any) {
      alert("Error editando: " + e.message);
    }
  };

  const statusConfig = (status: string) =>
    STATUS_CONFIG[status] || {
      label: status,
      color: "bg-gray-500/10 text-gray-400",
      icon: Clock,
    };

  const openVideoModal = (post: BufferPost) => {
    const source = post.assets?.[0]?.source;
    if (!source) return;
    setModalVideoUrl(source);
    setModalProxyUrl(
      `/content-api/proxy-video?url=${encodeURIComponent(source)}`
    );
    setModalTitle(
      post.text.slice(0, 60) + (post.text.length > 60 ? "..." : "")
    );
    setModalOpen(true);
  };

  const counts = useMemo(() => {
    const acc: Record<string, number> = { all: allPosts.length };
    for (const p of allPosts) acc[p.status] = (acc[p.status] || 0) + 1;
    return acc;
  }, [allPosts]);

  return (
    <div className="space-y-4">
      <RateLimitBanner snapshot={data} />

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
            <span className="ml-1.5 text-[10px] opacity-70">
              {counts[f.value] || 0}
            </span>
          </button>
        ))}
        {expiredIds.length > 0 && (
          <button
            onClick={handleCleanExpired}
            disabled={cleaning}
            className="ml-auto px-3 py-1.5 rounded-lg text-xs font-medium text-red-300 bg-red-500/10 border border-red-500/30 hover:bg-red-500/20 transition-colors disabled:opacity-50 inline-flex items-center gap-1.5"
            title="Borrar de Buffer todos los posts cuya media expiró"
          >
            {cleaning ? (
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
            ) : (
              <Sparkles className="w-3.5 h-3.5" />
            )}
            Limpiar {expiredIds.length} expirado{expiredIds.length === 1 ? "" : "s"}
          </button>
        )}
        <button
          onClick={refresh}
          disabled={loading}
          className={`${expiredIds.length > 0 ? "" : "ml-auto"} p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors disabled:opacity-50`}
          title="Refrescar"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
        </button>
      </div>

      {loading && allPosts.length === 0 && (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-6 h-6 animate-spin text-eko-blue" />
        </div>
      )}

      {!loading && allPosts.length === 0 && data?.error && !data.rate_limited && (
        <div className="rounded-xl border border-red-500/20 bg-red-500/5 p-4 text-red-400 text-sm">
          {data.error}
        </div>
      )}

      {!loading && posts.length === 0 && allPosts.length > 0 && (
        <div className="text-center py-12 text-gray-500">
          No hay posts con este filtro.
        </div>
      )}

      {!loading && allPosts.length === 0 && !data?.error && (
        <div className="text-center py-12 text-gray-500">
          Sin publicaciones todavía.
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {posts.map((post) => {
          const status = statusConfig(post.status);
          const StatusIcon = status.icon;
          const thumbnail = post.assets?.[0]?.thumbnail;
          const proxyUrl = thumbnail
            ? `/content-api/proxy-image?url=${encodeURIComponent(thumbnail)}`
            : null;
          const hasVideo = !!post.assets?.[0]?.source;
          const hasThumbnailUrl = !!thumbnail;
          const expired = isExpiredPost(post);
          // Only allow opening the player when the post has a playable source
          // AND its media hasn't been flagged as expired. Avoids the "video
          // not available" modal flash for legacy zombie posts.
          const clickable = hasVideo && !expired;

          return (
            <div
              key={post.id}
              className="rounded-xl border border-white/5 bg-white/[0.02] overflow-hidden hover:border-white/10 transition-colors"
            >
              <ThumbnailArea
                postId={post.id}
                proxyUrl={proxyUrl}
                clickable={clickable}
                hasThumbnailUrl={hasThumbnailUrl}
                isExpired={expired}
                onClick={() => clickable && openVideoModal(post)}
                onImgFailed={markImgFailed}
              />

              <div className="p-4">
                <div className="flex items-center gap-2 mb-2">
                  <span
                    className={`text-[10px] px-2 py-0.5 rounded-full border ${status.color}`}
                  >
                    <StatusIcon className="w-3 h-3 inline mr-1" />
                    {status.label}
                  </span>
                  <span className="text-[10px] text-gray-500 capitalize">
                    {post.channelService}
                  </span>
                </div>

                <p className="text-sm line-clamp-3 mb-2">{post.text}</p>

                {post.error?.message && (
                  <div className="mb-2 px-2 py-1.5 rounded-md bg-red-500/5 border border-red-500/15 text-[10px] text-red-300/90 leading-snug">
                    <span className="font-medium text-red-300">Motivo:</span>{" "}
                    {post.error.message.length > 140
                      ? post.error.message.slice(0, 140) + "…"
                      : post.error.message}
                  </div>
                )}

                <div className="flex items-center gap-1 text-[10px] text-gray-500 mb-3">
                  {post.dueAt && post.status === "scheduled" && (
                    <span>
                      Programado:{" "}
                      {new Date(post.dueAt).toLocaleString("es-CO", {
                        month: "short",
                        day: "numeric",
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </span>
                  )}
                  {post.sentAt && (
                    <span>
                      Publicado:{" "}
                      {new Date(post.sentAt).toLocaleString("es-CO", {
                        month: "short",
                        day: "numeric",
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </span>
                  )}
                  {!post.dueAt && !post.sentAt && (
                    <span>
                      Creado:{" "}
                      {new Date(post.createdAt).toLocaleDateString("es-CO")}
                    </span>
                  )}
                </div>

                <div className="flex items-center gap-1">
                  <button
                    onClick={() => handleEdit(post.id, post.text)}
                    className="p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
                    title="Editar texto"
                  >
                    <Pencil className="w-3.5 h-3.5" />
                  </button>
                  {/* For published posts, the externalLink is the most useful affordance — */}
                  {/* surface it as a labelled button rather than a cramped icon. */}
                  {post.externalLink && post.status === "sent" ? (
                    <a
                      href={post.externalLink}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-2.5 py-1 rounded-lg text-[11px] font-medium text-eko-green bg-eko-green/10 border border-eko-green/20 hover:bg-eko-green/20 transition-colors inline-flex items-center gap-1"
                      title="Abrir el post en la red social"
                    >
                      Ver en plataforma
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  ) : post.externalLink ? (
                    <a
                      href={post.externalLink}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
                      title="Ver en plataforma"
                    >
                      <ExternalLink className="w-3.5 h-3.5" />
                    </a>
                  ) : null}
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
      <VideoModal
        videoUrl={modalVideoUrl}
        proxyUrl={modalProxyUrl}
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        title={modalTitle}
      />
    </div>
  );
}

function ThumbnailArea({
  postId,
  proxyUrl,
  clickable,
  hasThumbnailUrl,
  isExpired,
  onClick,
  onImgFailed,
}: {
  postId: string;
  proxyUrl: string | null;
  clickable: boolean;
  hasThumbnailUrl: boolean;
  isExpired: boolean;
  onClick: () => void;
  onImgFailed: (postId: string) => void;
}) {
  // imgValid tracks whether the <img> successfully loaded. The proxy now
  // returns real HTTP errors (404 / 502) instead of a 1x1 PNG, so onError
  // fires correctly when the upstream media is gone.
  const [imgValid, setImgValid] = useState(true);

  const handleError = () => {
    setImgValid(false);
    onImgFailed(postId);
  };

  const showPlaceholder = !proxyUrl || !imgValid;
  // A post that *claims* a thumbnail URL but whose image failed to load is
  // treated as expired even when the post status is "sent" — typical when
  // the original asset lived on a temporary file host (litter.catbox.moe).
  const placeholderLabel = showPlaceholder
    ? isExpired || hasThumbnailUrl
      ? "Media expirado"
      : null
    : null;

  return (
    <div
      className={`aspect-video bg-black/30 relative overflow-hidden group ${
        clickable ? "cursor-pointer" : ""
      }`}
      onClick={clickable ? onClick : undefined}
      role={clickable ? "button" : undefined}
      tabIndex={clickable ? 0 : undefined}
      onKeyDown={
        clickable
          ? (e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                onClick();
              }
            }
          : undefined
      }
    >
      {proxyUrl && imgValid && (
        <img
          src={proxyUrl}
          alt=""
          className={`w-full h-full object-cover transition-transform duration-300 ${
            clickable ? "group-hover:scale-105" : ""
          }`}
          onError={handleError}
        />
      )}

      {clickable && imgValid && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity">
          <div className="w-12 h-12 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center border border-white/30">
            <Play className="w-5 h-5 text-white ml-0.5" fill="white" />
          </div>
        </div>
      )}

      {showPlaceholder && (
        <div className="absolute inset-0 flex flex-col items-center justify-center gap-2">
          <ImageOff className="w-8 h-8 text-gray-600" />
          {placeholderLabel ? (
            <span className="text-[10px] text-red-400/80 font-medium">
              {placeholderLabel}
            </span>
          ) : (
            <span className="text-[10px] text-gray-500 font-medium">
              Sin media
            </span>
          )}
        </div>
      )}
    </div>
  );
}
