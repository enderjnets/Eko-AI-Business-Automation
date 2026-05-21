"use client";

import { useEffect, useMemo, useState } from "react";
import {
  X,
  Send,
  Loader2,
  CheckCircle,
  AlertTriangle,
  Calendar,
  Clock,
  Zap,
  Music2,
  Camera,
  Facebook,
} from "lucide-react";
import { useBufferData, type BufferChannel } from "@/hooks/useBufferData";
import { useT } from "@/contexts/I18nProvider";

interface PublishModalProps {
  isOpen: boolean;
  onClose: () => void;
  video: {
    id: string;
    url: string;            // full public URL
    thumbnailUrl?: string | null;
    title?: string | null;
    isShort: boolean;
  } | null;
  onPublished?: () => void;
}

type Mode = "shareNow" | "addToQueue" | "customScheduled";

interface ChannelResult {
  channelId: string;
  service: string;
  ok: boolean;
  postId?: string;
  status?: string;
  error?: string;
}

const SUPPORTED_SERVICES = new Set(["tiktok", "instagram", "facebook"]);

const SERVICE_META: Record<
  string,
  { label: string; Icon: any; accent: string }
> = {
  tiktok: { label: "TikTok", Icon: Music2, accent: "text-white" },
  instagram: { label: "Instagram", Icon: Camera, accent: "text-pink-400" },
  facebook: { label: "Facebook", Icon: Facebook, accent: "text-blue-400" },
};

function defaultCaption(title?: string | null): string {
  if (!title) return "";
  return title.trim();
}

function toLocalDatetimeInput(d: Date): string {
  const pad = (n: number) => `${n}`.padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

export default function PublishModal({
  isOpen,
  onClose,
  video,
  onPublished,
}: PublishModalProps) {
  const { t } = useT();
  const { data: snapshot, loading: loadingChannels } = useBufferData();

  const channels = useMemo<BufferChannel[]>(() => {
    if (!snapshot?.channels) return [];
    return snapshot.channels.filter(
      (c) => !c.isDisconnected && SUPPORTED_SERVICES.has(c.service)
    );
  }, [snapshot]);

  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [caption, setCaption] = useState("");
  const [mode, setMode] = useState<Mode>("addToQueue");
  const [dueAtLocal, setDueAtLocal] = useState<string>(() =>
    toLocalDatetimeInput(new Date(Date.now() + 60 * 60 * 1000))
  );
  const [publishing, setPublishing] = useState(false);
  const [results, setResults] = useState<ChannelResult[] | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (isOpen) {
      setCaption(defaultCaption(video?.title));
      setMode("addToQueue");
      setResults(null);
      setError("");
      setDueAtLocal(
        toLocalDatetimeInput(new Date(Date.now() + 60 * 60 * 1000))
      );
    }
  }, [isOpen, video?.id, video?.title]);

  useEffect(() => {
    if (isOpen && channels.length && selectedIds.size === 0) {
      // default to all 3 selected
      setSelectedIds(new Set(channels.map((c) => c.id)));
    }
  }, [isOpen, channels, selectedIds.size]);

  if (!isOpen || !video) return null;

  const toggleChannel = (id: string) => {
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const canSubmit =
    selectedIds.size > 0 &&
    caption.trim().length > 0 &&
    !publishing &&
    (mode !== "customScheduled" || !!dueAtLocal);

  async function handlePublish() {
    if (!video) return;
    setPublishing(true);
    setError("");
    setResults(null);

    const selectedChannels = channels
      .filter((c) => selectedIds.has(c.id))
      .map((c) => ({ id: c.id, service: c.service }));

    let dueAtIso: string | undefined = undefined;
    if (mode === "customScheduled" && dueAtLocal) {
      const parsed = new Date(dueAtLocal);
      if (!isNaN(parsed.getTime())) dueAtIso = parsed.toISOString();
    }

    try {
      const r = await fetch("/content-api/publish", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          videoUrl: video.url,
          thumbnailUrl: video.thumbnailUrl || undefined,
          caption,
          channels: selectedChannels,
          mode,
          dueAt: dueAtIso,
          title: video.title || undefined,
          instagramType: video.isShort ? "reel" : "post",
          facebookType: video.isShort ? "reel" : "post",
        }),
      });
      const data = await r.json();
      if (data.error && !data.results) {
        throw new Error(data.error);
      }
      setResults(data.results || []);
      if (data.ok && onPublished) onPublished();
    } catch (e: any) {
      setError(e.message || "Failed to publish");
    } finally {
      setPublishing(false);
    }
  }

  const allOk = !!results && results.every((r) => r.ok);
  const anyOk = !!results && results.some((r) => r.ok);

  return (
    <div
      className="fixed inset-0 z-50 flex items-start sm:items-center justify-center bg-black/70 backdrop-blur-sm p-4 overflow-y-auto"
      onClick={onClose}
    >
      <div
        className="w-full max-w-2xl bg-eko-graphite border border-white/10 rounded-2xl shadow-2xl my-8"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-white/5">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-pink-500/10 text-pink-400">
              <Send className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-base font-semibold text-white">
                {t("content.publish.title")}
              </h2>
              <p className="text-xs text-gray-500 line-clamp-1">
                {video.title || video.id}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg text-gray-400 hover:text-white hover:bg-white/5"
            aria-label="Close"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Body */}
        <div className="px-6 py-5 space-y-5">
          {/* Channel selector */}
          <div>
            <label className="text-xs font-medium text-gray-400 mb-2 block">
              {t("content.publish.channels")}
            </label>
            {loadingChannels && !channels.length && (
              <div className="flex items-center gap-2 text-gray-500 text-sm py-3">
                <Loader2 className="w-4 h-4 animate-spin" />
                {t("content.publish.loading_channels")}
              </div>
            )}
            {!loadingChannels && channels.length === 0 && (
              <div className="text-sm text-yellow-400 bg-yellow-500/5 border border-yellow-500/20 rounded-lg p-3">
                {t("content.publish.no_channels")}
              </div>
            )}
            {channels.length > 0 && (
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                {channels.map((c) => {
                  const meta = SERVICE_META[c.service];
                  if (!meta) return null;
                  const Icon = meta.Icon;
                  const checked = selectedIds.has(c.id);
                  return (
                    <button
                      key={c.id}
                      type="button"
                      onClick={() => toggleChannel(c.id)}
                      disabled={publishing}
                      className={`flex items-center gap-2 px-3 py-2.5 rounded-lg border transition-colors text-left ${
                        checked
                          ? "bg-pink-500/10 border-pink-500/40 text-white"
                          : "bg-white/[0.02] border-white/10 text-gray-400 hover:bg-white/5"
                      }`}
                    >
                      <Icon className={`w-4 h-4 ${meta.accent}`} />
                      <div className="flex-1 min-w-0">
                        <p className="text-xs font-medium leading-tight">
                          {meta.label}
                        </p>
                        <p className="text-[10px] opacity-70 truncate">
                          {c.name}
                        </p>
                      </div>
                      {checked && (
                        <CheckCircle className="w-4 h-4 text-pink-400 flex-shrink-0" />
                      )}
                    </button>
                  );
                })}
              </div>
            )}
          </div>

          {/* Caption */}
          <div>
            <label className="text-xs font-medium text-gray-400 mb-2 block">
              {t("content.publish.caption")}
              <span className="text-[10px] text-gray-500 ml-1.5">
                {caption.length} {t("content.publish.chars")}
              </span>
            </label>
            <textarea
              value={caption}
              onChange={(e) => setCaption(e.target.value)}
              disabled={publishing}
              rows={4}
              placeholder={t("content.publish.caption_placeholder")}
              className="w-full bg-white/5 border border-white/10 rounded-lg px-3 py-2.5 text-sm text-white placeholder-gray-600 focus:outline-none focus:border-pink-400/50 resize-none"
            />
            <p className="text-[11px] text-gray-500 mt-1.5">
              {t("content.publish.caption_help")}
            </p>
          </div>

          {/* Mode */}
          <div>
            <label className="text-xs font-medium text-gray-400 mb-2 block">
              {t("content.publish.when")}
            </label>
            <div className="grid grid-cols-3 gap-2">
              {(
                [
                  {
                    id: "shareNow" as Mode,
                    label: t("content.publish.mode.now"),
                    Icon: Zap,
                  },
                  {
                    id: "addToQueue" as Mode,
                    label: t("content.publish.mode.queue"),
                    Icon: Clock,
                  },
                  {
                    id: "customScheduled" as Mode,
                    label: t("content.publish.mode.schedule"),
                    Icon: Calendar,
                  },
                ] as const
              ).map((opt) => {
                const active = mode === opt.id;
                const Icon = opt.Icon;
                return (
                  <button
                    key={opt.id}
                    type="button"
                    onClick={() => setMode(opt.id)}
                    disabled={publishing}
                    className={`flex flex-col items-center justify-center gap-1 px-3 py-3 rounded-lg border text-xs font-medium transition-colors ${
                      active
                        ? "bg-pink-500/10 border-pink-500/40 text-white"
                        : "bg-white/[0.02] border-white/10 text-gray-400 hover:bg-white/5"
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    {opt.label}
                  </button>
                );
              })}
            </div>
            {mode === "customScheduled" && (
              <input
                type="datetime-local"
                value={dueAtLocal}
                onChange={(e) => setDueAtLocal(e.target.value)}
                disabled={publishing}
                min={toLocalDatetimeInput(new Date())}
                className="mt-3 w-full bg-white/5 border border-white/10 rounded-lg px-3 py-2.5 text-sm text-white focus:outline-none focus:border-pink-400/50"
              />
            )}
          </div>

          {/* Results / errors */}
          {error && (
            <div className="flex items-start gap-2 text-sm text-red-400 bg-red-500/5 border border-red-500/20 rounded-lg p-3">
              <AlertTriangle className="w-4 h-4 flex-shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}
          {results && (
            <div className="space-y-2">
              <div
                className={`text-xs font-medium ${
                  allOk
                    ? "text-eko-green"
                    : anyOk
                    ? "text-yellow-400"
                    : "text-red-400"
                }`}
              >
                {allOk
                  ? t("content.publish.result.all_ok")
                  : anyOk
                  ? t("content.publish.result.partial")
                  : t("content.publish.result.all_failed")}
              </div>
              <ul className="space-y-1.5">
                {results.map((r) => {
                  const meta = SERVICE_META[r.service];
                  const Icon = meta?.Icon || Send;
                  return (
                    <li
                      key={r.channelId}
                      className="flex items-start gap-2 px-3 py-2 rounded-lg bg-white/[0.02] border border-white/5 text-xs"
                    >
                      <Icon
                        className={`w-4 h-4 flex-shrink-0 mt-0.5 ${
                          meta?.accent || "text-gray-400"
                        }`}
                      />
                      <div className="flex-1 min-w-0">
                        <p className="text-gray-300 font-medium">
                          {meta?.label || r.service}
                        </p>
                        {r.ok ? (
                          <p className="text-eko-green text-[11px]">
                            {t("content.publish.result.posted")} ·{" "}
                            {r.status || "ok"}
                          </p>
                        ) : (
                          <p className="text-red-400 text-[11px]">
                            {r.error}
                          </p>
                        )}
                      </div>
                      {r.ok ? (
                        <CheckCircle className="w-4 h-4 text-eko-green flex-shrink-0" />
                      ) : (
                        <AlertTriangle className="w-4 h-4 text-red-400 flex-shrink-0" />
                      )}
                    </li>
                  );
                })}
              </ul>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end gap-2 px-6 py-4 border-t border-white/5">
          <button
            onClick={onClose}
            disabled={publishing}
            className="px-4 py-2 rounded-lg text-sm text-gray-400 hover:text-white hover:bg-white/5 transition-colors"
          >
            {results && allOk ? t("content.publish.close") : t("content.publish.cancel")}
          </button>
          {!(results && allOk) && (
            <button
              onClick={handlePublish}
              disabled={!canSubmit}
              className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium bg-gradient-to-r from-pink-500 to-pink-600 text-white hover:from-pink-600 hover:to-pink-700 transition-all disabled:opacity-40 disabled:cursor-not-allowed"
            >
              {publishing ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Send className="w-4 h-4" />
              )}
              {publishing
                ? t("content.publish.publishing")
                : results
                ? t("content.publish.retry")
                : t("content.publish.publish_cta")}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
