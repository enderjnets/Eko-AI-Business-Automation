"use client";

import { useEffect, useState, useMemo } from "react";
import {
  format,
  startOfMonth,
  endOfMonth,
  startOfWeek,
  endOfWeek,
  eachDayOfInterval,
  isSameMonth,
  isSameDay,
  addMonths,
  subMonths,
  isToday,
} from "date-fns";
import { es } from "date-fns/locale";
import {
  ChevronLeft,
  ChevronRight,
  CalendarDays,
  X,
  Clock,
  CheckCircle,
  Send,
  AlertTriangle,
  Pencil,
  ImageOff,
  Trash2,
  Play,
} from "lucide-react";
import VideoModal from "./VideoModal";

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

const SERVICE_COLORS: Record<string, string> = {
  tiktok: "bg-white",
  instagram: "bg-pink-400",
  facebook: "bg-blue-400",
};

const STATUS_ICON: Record<string, React.ReactNode> = {
  sent: <CheckCircle className="w-3 h-3 text-eko-green" />,
  scheduled: <Clock className="w-3 h-3 text-yellow-400" />,
  sending: <Send className="w-3 h-3 text-eko-blue" />,
  error: <AlertTriangle className="w-3 h-3 text-red-400" />,
  draft: <Pencil className="w-3 h-3 text-gray-400" />,
};

export default function PostCalendar() {
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedDay, setSelectedDay] = useState<Date | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [modalVideoUrl, setModalVideoUrl] = useState("");
  const [modalProxyUrl, setModalProxyUrl] = useState("");
  const [modalTitle, setModalTitle] = useState("");

  const monthStart = startOfMonth(currentMonth);
  const monthEnd = endOfMonth(monthStart);
  const calendarStart = startOfWeek(monthStart, { weekStartsOn: 1 });
  const calendarEnd = endOfWeek(monthEnd, { weekStartsOn: 1 });
  const days = eachDayOfInterval({ start: calendarStart, end: calendarEnd });

  // Fetch posts for the visible month range (plus buffer)
  useEffect(() => {
    setLoading(true);
    const start = format(subMonths(monthStart, 1), "yyyy-MM-dd");
    const end = format(addMonths(monthEnd, 1), "yyyy-MM-dd");

    fetch(`/content-api/posts?limit=100&startDate=${start}&endDate=${end}`)
      .then((r) => r.json())
      .then((data) => {
        if (data.error) throw new Error(data.error);
        setPosts(data.posts || []);
        setError("");
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [currentMonth]);

  const postsByDay = useMemo(() => {
    const map = new Map<string, Post[]>();
    for (const post of posts) {
      const dateStr = post.dueAt
        ? post.dueAt.split("T")[0]
        : post.sentAt
        ? post.sentAt.split("T")[0]
        : post.createdAt.split("T")[0];
      if (!map.has(dateStr)) map.set(dateStr, []);
      map.get(dateStr)!.push(post);
    }
    return map;
  }, [posts]);

  const selectedDayPosts = selectedDay
    ? postsByDay.get(format(selectedDay, "yyyy-MM-dd")) || []
    : [];

  const weekDays = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"];

  const openVideoModal = (post: Post) => {
    const source = post.assets?.[0]?.source;
    if (!source) return;
    setModalVideoUrl(source);
    setModalProxyUrl(`/content-api/proxy-video?url=${encodeURIComponent(source)}`);
    setModalTitle(post.text.slice(0, 60) + (post.text.length > 60 ? "..." : ""));
    setModalOpen(true);
  };

  const handleDelete = async (id: string) => {
    if (!confirm("¿Seguro que quieres borrar este post?")) return;
    try {
      const res = await fetch(`/content-api/posts/${id}/delete`, { method: "POST" });
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      setPosts((prev) => prev.filter((p) => p.id !== id));
    } catch (e: any) {
      alert("Error borrando: " + e.message);
    }
  };

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <CalendarDays className="w-5 h-5 text-pink-400" />
          <h3 className="text-sm font-medium text-gray-400">
            {format(currentMonth, "MMMM yyyy", { locale: es })}
          </h3>
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={() => setCurrentMonth(subMonths(currentMonth, 1))}
            className="p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <button
            onClick={() => setCurrentMonth(new Date())}
            className="px-3 py-1 rounded-lg text-xs font-medium text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
          >
            Hoy
          </button>
          <button
            onClick={() => setCurrentMonth(addMonths(currentMonth, 1))}
            className="p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      {loading && (
        <div className="flex items-center justify-center py-12">
          <div className="w-6 h-6 border-2 border-eko-blue border-t-transparent rounded-full animate-spin" />
        </div>
      )}

      {error && (
        <div className="rounded-xl border border-red-500/20 bg-red-500/5 p-4 text-red-400 text-sm">
          {error}
        </div>
      )}

      {!loading && !error && (
        <>
          {/* Weekday headers */}
          <div className="grid grid-cols-7 gap-1">
            {weekDays.map((d) => (
              <div
                key={d}
                className="text-center text-xs text-gray-500 font-medium py-2"
              >
                {d}
              </div>
            ))}
          </div>

          {/* Calendar grid */}
          <div className="grid grid-cols-7 gap-1">
            {days.map((day) => {
              const dateStr = format(day, "yyyy-MM-dd");
              const dayPosts = postsByDay.get(dateStr) || [];
              const services = Array.from(
                new Set(dayPosts.map((p) => p.channelService))
              );
              const isCurrentMonth = isSameMonth(day, currentMonth);
              const isTodayDate = isToday(day);
              const isSelected = selectedDay && isSameDay(day, selectedDay);

              return (
                <button
                  key={dateStr}
                  onClick={() =>
                    setSelectedDay(isSelected ? null : day)
                  }
                  className={`relative aspect-square rounded-lg border p-1.5 text-left transition-all ${
                    isCurrentMonth
                      ? "bg-white/[0.02] border-white/5 hover:bg-white/[0.05]"
                      : "bg-transparent border-transparent opacity-30"
                  } ${isTodayDate ? "ring-1 ring-pink-400/50" : ""} ${
                    isSelected ? "bg-white/[0.06] border-pink-400/30" : ""
                  }`}
                >
                  <span
                    className={`text-xs font-medium ${
                      isTodayDate
                        ? "text-pink-400"
                        : isCurrentMonth
                        ? "text-gray-300"
                        : "text-gray-600"
                    }`}
                  >
                    {format(day, "d")}
                  </span>

                  {dayPosts.length > 0 && (
                    <div className="absolute bottom-1.5 left-1.5 right-1.5 flex flex-wrap gap-1">
                      {services.slice(0, 3).map((svc) => (
                        <div
                          key={svc}
                          className={`w-1.5 h-1.5 rounded-full ${
                            SERVICE_COLORS[svc] || "bg-gray-500"
                          }`}
                        />
                      ))}
                      {dayPosts.length > 3 && (
                        <span className="text-[8px] text-gray-500 leading-none">
                          +{dayPosts.length - 3}
                        </span>
                      )}
                    </div>
                  )}

                  {/* Tooltip-ish count on hover */}
                  {dayPosts.length > 0 && (
                    <div className="absolute top-1.5 right-1.5">
                      <span className="text-[9px] text-gray-500">
                        {dayPosts.length}
                      </span>
                    </div>
                  )}
                </button>
              );
            })}
          </div>

          {/* Day detail drawer */}
          {selectedDay && (
            <div className="rounded-xl border border-white/5 bg-white/[0.02] p-4">
              <div className="flex items-center justify-between mb-3">
                <h4 className="text-sm font-medium">
                  {format(selectedDay, "EEEE d 'de' MMMM", { locale: es })}
                </h4>
                <button
                  onClick={() => setSelectedDay(null)}
                  className="p-1 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              {selectedDayPosts.length === 0 ? (
                <p className="text-sm text-gray-500">Sin publicaciones este día.</p>
              ) : (
                <div className="space-y-3 max-h-80 overflow-y-auto">
                  {selectedDayPosts.map((post) => {
                    const thumbnail = post.assets?.[0]?.thumbnail;
                    const proxyUrl = thumbnail ? `/content-api/proxy-image?url=${encodeURIComponent(thumbnail)}` : null;
                    const isError = post.status === "error";
                    const hasVideo = !!post.assets?.[0]?.source;

                    return (
                      <div
                        key={post.id}
                        className={`flex gap-3 rounded-lg p-3 ${
                          isError ? "bg-red-500/5 border border-red-500/10" : "bg-white/5"
                        }`}
                      >
                        <CalendarThumbnail
                          proxyUrl={proxyUrl}
                          hasVideo={hasVideo}
                          isExpired={isError}
                          onClick={() => hasVideo && openVideoModal(post)}
                        />
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="text-[10px] capitalize text-gray-400">
                              {post.channelService}
                            </span>
                            {STATUS_ICON[post.status] || (
                              <Clock className="w-3 h-3 text-gray-400" />
                            )}
                            {isError && (
                              <span className="text-[10px] text-red-400">Error</span>
                            )}
                          </div>
                          <p className="text-sm line-clamp-2">{post.text}</p>
                          {post.error?.message && (
                            <p className="text-[10px] text-red-400/80 mt-1 line-clamp-2">
                              {post.error.message}
                            </p>
                          )}
                        </div>
                        <button
                          onClick={() => handleDelete(post.id)}
                          className="p-1.5 rounded-lg text-gray-500 hover:text-red-400 hover:bg-red-500/10 transition-colors self-start"
                          title="Borrar post"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          )}
        </>
      )}
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

function CalendarThumbnail({
  proxyUrl,
  hasVideo,
  isExpired,
  onClick,
}: {
  proxyUrl: string | null;
  hasVideo: boolean;
  isExpired: boolean;
  onClick: () => void;
}) {
  const [imgValid, setImgValid] = useState(true);

  const handleLoad = (e: React.SyntheticEvent<HTMLImageElement>) => {
    const img = e.currentTarget;
    if (img.naturalWidth < 2 && img.naturalHeight < 2) {
      setImgValid(false);
    }
  };

  const showPlaceholder = !proxyUrl || !imgValid;

  return (
    <div
      className={`w-16 h-16 rounded-lg overflow-hidden flex-shrink-0 relative ${
        hasVideo && !showPlaceholder ? "cursor-pointer group" : ""
      } ${showPlaceholder ? "bg-white/5" : ""}`}
      onClick={onClick}
      role={hasVideo ? "button" : undefined}
      tabIndex={hasVideo ? 0 : undefined}
      onKeyDown={hasVideo ? (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); onClick(); } } : undefined}
    >
      {proxyUrl && imgValid && (
        <img
          src={proxyUrl}
          alt=""
          className="w-full h-full object-cover"
          onLoad={handleLoad}
          onError={() => setImgValid(false)}
        />
      )}
      {hasVideo && !showPlaceholder && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/30 opacity-0 group-hover:opacity-100 transition-opacity">
          <Play className="w-5 h-5 text-white" fill="white" />
        </div>
      )}
      {showPlaceholder && (
        <div className="w-full h-full flex flex-col items-center justify-center gap-1">
          <ImageOff className="w-5 h-5 text-gray-600" />
          {isExpired && <span className="text-[8px] text-red-400/70">Expirado</span>}
        </div>
      )}
    </div>
  );
}
