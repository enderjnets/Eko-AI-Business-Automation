"use client";

import { useState, useEffect } from "react";
import {
  Calendar as CalendarIcon,
  Clock,
  Video,
  MapPin,
  Phone,
  X,
  CheckCircle,
  AlertCircle,
  Loader2,
  User,
  Mail,
  Target,
  Lightbulb,
  ShieldAlert,
  ExternalLink,
  ArrowRight,
} from "lucide-react";
import Navbar from "@/components/Navbar";
import { calendarApi } from "@/lib/api";

interface LeadSnippet {
  id: number;
  business_name: string;
  category?: string | null;
  city?: string | null;
  pain_points?: string[] | null;
  services?: string[] | null;
  total_score?: number | null;
  description?: string | null;
  scoring_reason?: string | null;
  review_summary?: string | null;
  proposal_suggestion?: string | null;
}

interface Booking {
  id: number;
  title: string;
  start_time: string;
  end_time: string | null;
  status: string;
  attendee_name: string;
  attendee_email: string;
  location: string | null;
  location_type: string | null;
  notes: string | null;
  lead_id: number;
  lead?: LeadSnippet | null;
  meta?: Record<string, any> | null;
}

export default function CalendarPage() {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [filter, setFilter] = useState<"upcoming" | "all" | "past">("upcoming");
  const [cancellingId, setCancellingId] = useState<number | null>(null);
  const [selectedBooking, setSelectedBooking] = useState<Booking | null>(null);

  useEffect(() => {
    loadBookings();
  }, [filter]);

  const loadBookings = async () => {
    setIsLoading(true);
    try {
      const params: any = {};
      if (filter === "upcoming") params.upcoming = true;
      const res = await calendarApi.listBookings(params);
      setBookings(res.data);
    } catch (err) {
      console.error("Failed to load bookings:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = async (id: number) => {
    if (!confirm("Cancel this meeting?")) return;
    setCancellingId(id);
    try {
      await calendarApi.cancelBooking(id, "Cancelled by user");
      await loadBookings();
    } catch (err) {
      console.error("Failed to cancel:", err);
    } finally {
      setCancellingId(null);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "confirmed":
        return "bg-green-500/10 text-green-400 border-green-500/20";
      case "pending":
        return "bg-yellow-500/10 text-yellow-400 border-yellow-500/20";
      case "cancelled":
        return "bg-red-500/10 text-red-400 border-red-500/20";
      case "completed":
        return "bg-blue-500/10 text-blue-400 border-blue-500/20";
      default:
        return "bg-gray-500/10 text-gray-400 border-gray-500/20";
    }
  };

  const getLocationIcon = (type: string | null) => {
    switch (type) {
      case "video":
        return <Video className="w-4 h-4" />;
      case "phone":
        return <Phone className="w-4 h-4" />;
      case "in_person":
        return <MapPin className="w-4 h-4" />;
      default:
        return <Video className="w-4 h-4" />;
    }
  };

  const formatDate = (iso: string) => {
    const d = new Date(iso);
    return d.toLocaleDateString("en-US", {
      weekday: "short",
      month: "short",
      day: "numeric",
    });
  };

  const formatTime = (iso: string) => {
    const d = new Date(iso);
    return d.toLocaleTimeString("en-US", {
      hour: "numeric",
      minute: "2-digit",
    });
  };

  const formatFullDate = (iso: string) => {
    const d = new Date(iso);
    return d.toLocaleDateString("en-US", {
      weekday: "long",
      month: "long",
      day: "numeric",
      year: "numeric",
    });
  };

  const renderMarkdownLike = (text: string | null) => {
    if (!text) return null;
    // Simple formatting: split by lines, bold headers, bullet points
    const lines = text.split("\n");
    return (
      <div className="space-y-2">
        {lines.map((line, idx) => {
          const trimmed = line.trim();
          if (!trimmed) return <div key={idx} className="h-2" />;
          if (trimmed.startsWith("## ")) {
            return (
              <h4 key={idx} className="text-sm font-semibold text-white mt-3 first:mt-0">
                {trimmed.replace("## ", "")}
              </h4>
            );
          }
          if (trimmed.startsWith("- ")) {
            return (
              <li key={idx} className="text-sm text-gray-300 ml-4">
                {trimmed.replace("- ", "")}
              </li>
            );
          }
          return (
            <p key={idx} className="text-sm text-gray-300">
              {trimmed}
            </p>
          );
        })}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-eko-graphite">
      <Navbar />

      <main className="pt-20 pb-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold font-display">Calendar</h1>
            <p className="text-gray-400 text-sm mt-1">
              Meetings and appointments
            </p>
          </div>

          {/* Filter tabs */}
          <div className="flex items-center gap-1 bg-white/5 rounded-lg p-1">
            {(["upcoming", "all", "past"] as const).map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-3 py-1.5 rounded-md text-sm capitalize transition-colors ${
                  filter === f
                    ? "bg-white/10 text-white"
                    : "text-gray-400 hover:text-white"
                }`}
              >
                {f}
              </button>
            ))}
          </div>
        </div>

        {/* Bookings list */}
        {isLoading ? (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="w-8 h-8 animate-spin text-eko-blue" />
          </div>
        ) : bookings.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 text-gray-500">
            <CalendarIcon className="w-12 h-12 mb-4 opacity-50" />
            <p className="text-lg font-medium">No meetings found</p>
            <p className="text-sm">
              {filter === "upcoming"
                ? "No upcoming meetings scheduled"
                : "No meetings match this filter"}
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {bookings.map((booking) => (
              <div
                key={booking.id}
                onClick={() => setSelectedBooking(booking)}
                className="rounded-xl border border-white/10 bg-white/5 p-5 hover:border-white/20 hover:bg-white/[0.07] transition-colors cursor-pointer"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="font-semibold text-white">
                        {booking.title}
                      </h3>
                      <span
                        className={`px-2 py-0.5 rounded-full text-xs border capitalize ${getStatusColor(
                          booking.status
                        )}`}
                      >
                        {booking.status}
                      </span>
                    </div>

                    <div className="flex flex-wrap items-center gap-4 text-sm text-gray-400">
                      <div className="flex items-center gap-1.5">
                        <CalendarIcon className="w-4 h-4" />
                        <span>{formatDate(booking.start_time)}</span>
                      </div>
                      <div className="flex items-center gap-1.5">
                        <Clock className="w-4 h-4" />
                        <span>
                          {formatTime(booking.start_time)}
                          {booking.end_time &&
                            ` - ${formatTime(booking.end_time)}`}
                        </span>
                      </div>
                      <div className="flex items-center gap-1.5">
                        {getLocationIcon(booking.location_type)}
                        <span className="capitalize">
                          {booking.location_type || "Video"}
                        </span>
                      </div>
                    </div>

                    <div className="flex items-center gap-4 mt-3 text-sm">
                      <div className="flex items-center gap-1.5 text-gray-400">
                        <User className="w-4 h-4" />
                        <span>{booking.attendee_name}</span>
                      </div>
                      <div className="flex items-center gap-1.5 text-gray-400">
                        <Mail className="w-4 h-4" />
                        <span>{booking.attendee_email}</span>
                      </div>
                    </div>

                    {booking.notes && (
                      <p className="mt-2 text-sm text-gray-500 line-clamp-2">
                        {booking.notes.substring(0, 120)}
                        {booking.notes.length > 120 ? "..." : ""}
                      </p>
                    )}

                    {booking.location && booking.status !== "cancelled" && (
                      <a
                        href={booking.location}
                        target="_blank"
                        rel="noopener noreferrer"
                        onClick={(e) => e.stopPropagation()}
                        className="inline-flex items-center gap-1.5 mt-3 text-sm text-eko-blue hover:text-eko-blue-dark"
                      >
                        <CheckCircle className="w-4 h-4" />
                        Join meeting
                      </a>
                    )}
                  </div>

                  {booking.status !== "cancelled" &&
                    booking.status !== "completed" && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleCancel(booking.id);
                        }}
                        disabled={cancellingId === booking.id}
                        className="p-2 rounded-lg text-gray-400 hover:text-red-400 hover:bg-red-500/10 transition-colors disabled:opacity-50"
                        title="Cancel meeting"
                      >
                        {cancellingId === booking.id ? (
                          <Loader2 className="w-4 h-4 animate-spin" />
                        ) : (
                          <X className="w-4 h-4" />
                        )}
                      </button>
                    )}
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      {/* Booking Detail Modal */}
      {selectedBooking && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
          onClick={() => setSelectedBooking(null)}
        >
          <div
            className="w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-2xl border border-white/10 bg-eko-graphite shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Modal Header */}
            <div className="flex items-start justify-between p-6 border-b border-white/10">
              <div>
                <div className="flex items-center gap-3 mb-1">
                  <h2 className="text-xl font-bold text-white">
                    {selectedBooking.title}
                  </h2>
                  <span
                    className={`px-2 py-0.5 rounded-full text-xs border capitalize ${getStatusColor(
                      selectedBooking.status
                    )}`}
                  >
                    {selectedBooking.status}
                  </span>
                </div>
                <p className="text-gray-400 text-sm">
                  {formatFullDate(selectedBooking.start_time)} ·{" "}
                  {formatTime(selectedBooking.start_time)}
                  {selectedBooking.end_time &&
                    ` - ${formatTime(selectedBooking.end_time)}`}
                </p>
              </div>
              <button
                onClick={() => setSelectedBooking(null)}
                className="p-2 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6 space-y-6">
              {/* Meeting Details */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="flex items-center gap-3 p-3 rounded-lg bg-white/5">
                  <div className="p-2 rounded-md bg-white/10">
                    <User className="w-4 h-4 text-eko-blue" />
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Attendee</p>
                    <p className="text-sm text-white font-medium">
                      {selectedBooking.attendee_name}
                    </p>
                    <p className="text-xs text-gray-400">
                      {selectedBooking.attendee_email}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3 p-3 rounded-lg bg-white/5">
                  <div className="p-2 rounded-md bg-white/10">
                    {getLocationIcon(selectedBooking.location_type)}
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Location</p>
                    <p className="text-sm text-white font-medium capitalize">
                      {selectedBooking.location_type || "Video"}
                    </p>
                    {selectedBooking.location &&
                      selectedBooking.status !== "cancelled" && (
                        <a
                          href={selectedBooking.location}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-1 text-xs text-eko-blue hover:underline"
                        >
                          Join meeting <ExternalLink className="w-3 h-3" />
                        </a>
                      )}
                  </div>
                </div>
              </div>

              {/* Lead Snapshot */}
              {selectedBooking.lead && (
                <div className="rounded-xl border border-white/10 bg-white/[0.03] p-4">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                      <Target className="w-4 h-4 text-eko-blue" />
                      Lead Snapshot
                    </h3>
                    <a
                      href={`/leads/${selectedBooking.lead.id}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-xs text-eko-blue hover:underline flex items-center gap-1"
                    >
                      View lead <ArrowRight className="w-3 h-3" />
                    </a>
                  </div>

                  <div className="flex flex-wrap items-center gap-2 mb-3">
                    <span className="text-white font-medium">
                      {selectedBooking.lead.business_name}
                    </span>
                    {selectedBooking.lead.category && (
                      <span className="px-2 py-0.5 rounded-full text-xs bg-white/10 text-gray-300">
                        {selectedBooking.lead.category}
                      </span>
                    )}
                    {selectedBooking.lead.city && (
                      <span className="px-2 py-0.5 rounded-full text-xs bg-white/10 text-gray-300">
                        {selectedBooking.lead.city}
                      </span>
                    )}
                    {selectedBooking.lead.total_score !== null &&
                      selectedBooking.lead.total_score !== undefined && (
                        <span className="px-2 py-0.5 rounded-full text-xs bg-eko-blue/20 text-eko-blue">
                          Score: {selectedBooking.lead.total_score}/100
                        </span>
                      )}
                  </div>

                  {selectedBooking.lead.description && (
                    <p className="text-sm text-gray-400 mb-3 line-clamp-3">
                      {selectedBooking.lead.description}
                    </p>
                  )}

                  <div className="flex flex-wrap gap-2">
                    {selectedBooking.lead.pain_points?.map((pp, i) => (
                      <span
                        key={i}
                        className="px-2 py-0.5 rounded-md text-xs bg-red-500/10 text-red-400 border border-red-500/20"
                      >
                        {pp}
                      </span>
                    ))}
                    {selectedBooking.lead.services?.map((s, i) => (
                      <span
                        key={`s-${i}`}
                        className="px-2 py-0.5 rounded-md text-xs bg-green-500/10 text-green-400 border border-green-500/20"
                      >
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* AI Sales Brief */}
              {(selectedBooking.notes ||
                selectedBooking.meta?.sales_brief) && (
                <div className="rounded-xl border border-white/10 bg-white/[0.03] p-4">
                  <h3 className="text-sm font-semibold text-white flex items-center gap-2 mb-3">
                    <Lightbulb className="w-4 h-4 text-yellow-400" />
                    AI Sales Brief
                  </h3>
                  {renderMarkdownLike(
                    selectedBooking.meta?.sales_brief || selectedBooking.notes
                  )}
                </div>
              )}

              {/* Raw Notes fallback */}
              {selectedBooking.notes && !selectedBooking.meta?.sales_brief && (
                <div className="rounded-xl border border-white/10 bg-white/[0.03] p-4">
                  <h3 className="text-sm font-semibold text-white flex items-center gap-2 mb-3">
                    <ShieldAlert className="w-4 h-4 text-orange-400" />
                    Notes
                  </h3>
                  <p className="text-sm text-gray-300 whitespace-pre-wrap">
                    {selectedBooking.notes}
                  </p>
                </div>
              )}
            </div>

            {/* Modal Footer */}
            <div className="flex items-center justify-end gap-3 p-6 border-t border-white/10">
              <button
                onClick={() => setSelectedBooking(null)}
                className="px-4 py-2 rounded-lg text-sm text-gray-300 hover:text-white hover:bg-white/10 transition-colors"
              >
                Close
              </button>
              {selectedBooking.status !== "cancelled" &&
                selectedBooking.status !== "completed" && (
                  <button
                    onClick={() => {
                      handleCancel(selectedBooking.id);
                      setSelectedBooking(null);
                    }}
                    disabled={cancellingId === selectedBooking.id}
                    className="px-4 py-2 rounded-lg text-sm bg-red-500/10 text-red-400 hover:bg-red-500/20 border border-red-500/20 transition-colors disabled:opacity-50"
                  >
                    Cancel Meeting
                  </button>
                )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
