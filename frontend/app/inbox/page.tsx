"use client";

import { useState, useEffect, useCallback } from "react";

// Strip HTML tags for clean preview text
function stripHtml(html: string): string {
  if (!html) return "";
  return html.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
}
import {
  Inbox,
  MailOpen,
  Mail,
  Loader2,
  Zap,
  CheckCircle,
  AlertCircle,
  Clock,
  ChevronDown,
  ChevronUp,
  Send,
  Smile,
  Meh,
  Frown,
  MessageSquare,
  Wand2,
  X,
  Edit3,
  ArrowLeft,
  Trash2,
} from "lucide-react";
import Navbar from "@/components/Navbar";
import { emailsApi } from "@/lib/api";
import { useT } from "@/contexts/I18nProvider";

interface InboxItem {
  id: number;
  lead_id: number;
  lead_name: string;
  lead_email: string;
  lead_status: string;
  subject: string;
  content: string;
  direction: string;
  sentiment: string;
  intent: string;
  summary: string;
  next_action: string;
  priority: string;
  key_points: string[];
  read: boolean;
  auto_status_changed: boolean;
  previous_status: string;
  created_at: string;
  lead_unread_count?: number;
  lead_total_count?: number;
}

interface AIReply {
  subject: string;
  body: string;
  tone: string;
  confidence: number;
  suggested_next_action: string;
}

interface ConversationItem {
  id: number;
  direction: string;
  subject: string;
  content: string;
  created_at: string;
  lead_unread_count?: number;
  lead_total_count?: number;
}

export default function InboxPage() {
  const [items, setItems] = useState<InboxItem[]>([]);
  const { t } = useT();
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<"all" | "unread" | "high_priority">("all");
  const [folder, setFolder] = useState<"inbox" | "sent" | "all" | "drafts">("inbox");
  const [expandedId, setExpandedId] = useState<number | null>(null);
  const [markingRead, setMarkingRead] = useState<number | null>(null);
  const [simulating, setSimulating] = useState(false);

  // Delete state
  const [selectedIds, setSelectedIds] = useState<Set<number>>(new Set());
  const [deletingIds, setDeletingIds] = useState<Set<number>>(new Set());
  const [bulkDeleting, setBulkDeleting] = useState(false);

  // AI Reply state
  const [showReplyModal, setShowReplyModal] = useState(false);
  const [replyTarget, setReplyTarget] = useState<InboxItem | null>(null);
  const [generatingReply, setGeneratingReply] = useState(false);
  const [aiReply, setAiReply] = useState<AIReply | null>(null);
  const [editedSubject, setEditedSubject] = useState("");
  const [editedBody, setEditedBody] = useState("");
  const [sendingReply, setSendingReply] = useState(false);
  const [replyTone, setReplyTone] = useState("professional");
  const [replyLength, setReplyLength] = useState("medium");
  const [replyError, setReplyError] = useState("");
  const [conversation, setConversation] = useState<ConversationItem[]>([]);
  const [loadingConversation, setLoadingConversation] = useState(false);

  // Quick manual reply state
  const [quickReplySubject, setQuickReplySubject] = useState("");
  const [quickReplyBody, setQuickReplyBody] = useState("");
  const [sendingQuickReply, setSendingQuickReply] = useState(false);
  const [quickReplyError, setQuickReplyError] = useState("");
  const [quickReplyAttachments, setQuickReplyAttachments] = useState<File[]>([]);

  // Forward state
  const [showForward, setShowForward] = useState(false);
  const [forwardEmail, setForwardEmail] = useState("");
  const [forwardNote, setForwardNote] = useState("");
  const [sendingForward, setSendingForward] = useState(false);
  const [forwardError, setForwardError] = useState("");

  // Draft state
  const [savingDraft, setSavingDraft] = useState(false);
  const [draftError, setDraftError] = useState("");

  const loadInbox = useCallback(async () => {
    setLoading(true);
    try {
      const params: any = {};
      if (filter === "unread") params.status = "unread";
      if (folder === "inbox") params.direction = "inbound";
      else if (folder === "sent") params.direction = "outbound";
      else if (folder === "drafts") params.direction = "draft";
      // folder === "all" → no direction filter
      const res = await emailsApi.inbox(params);
      let data = res.data?.items || [];
      if (filter === "high_priority") {
        data = data.filter((i: InboxItem) => i.priority === "high");
      }
      setItems(data);
    } catch (err) {
      console.error("Failed to load inbox:", err);
    } finally {
      setLoading(false);
    }
  }, [filter, folder]);

  useEffect(() => {
    loadInbox();
    // Auto-refresh every 30 seconds for real-time inbox
    const interval = setInterval(() => {
      loadInbox();
    }, 30000);
    return () => clearInterval(interval);
  }, [loadInbox]);

  const handleMarkRead = async (id: number) => {
    setMarkingRead(id);
    try {
      await emailsApi.markRead(id);
      setItems((prev) =>
        prev.map((item) => (item.id === id ? { ...item, read: true } : item))
      );
    } catch (err) {
      console.error(err);
    } finally {
      setMarkingRead(null);
    }
  };

  const handleSimulateReply = async () => {
    const leadId = prompt(t("inbox.simulate.lead_id_prompt"));
    if (!leadId) return;
    const subject = prompt(t("inbox.simulate.subject_prompt"), t("inbox.simulate.subject_default"));
    if (!subject) return;
    const body = prompt(
      t("inbox.simulate.body_prompt"),
      t("inbox.simulate.body_default")
    );
    if (!body) return;

    setSimulating(true);
    try {
      await emailsApi.simulateReply(parseInt(leadId), subject, body);
      loadInbox();
    } catch (err) {
      console.error(err);
      alert(t("inbox.simulate.error"));
    } finally {
      setSimulating(false);
    }
  };

  const openReplyModal = async (item: InboxItem) => {
    setReplyTarget(item);
    setShowReplyModal(true);
    setAiReply(null);
    setEditedSubject("");
    setEditedBody("");
    setReplyError("");
    setReplyTone("professional");
    setReplyLength("medium");

    // Load conversation
    setLoadingConversation(true);
    try {
      const res = await emailsApi.conversation(item.id);
      setConversation(res.data?.items || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingConversation(false);
    }
  };

  const handleGenerateReply = async () => {
    if (!replyTarget) return;
    setGeneratingReply(true);
    setReplyError("");
    try {
      const res = await emailsApi.aiReply(replyTarget.id, {
        tone: replyTone,
        max_length: replyLength,
      });
      const reply = res.data?.reply;
      setAiReply(reply);
      setEditedSubject(reply?.subject || "");
      setEditedBody(reply?.body || "");
    } catch (err: any) {
      setReplyError(err.response?.data?.detail || t("inbox.error.generate_reply"));
    } finally {
      setGeneratingReply(false);
    }
  };

  const handleSendReply = async () => {
    if (!replyTarget) return;
    setSendingReply(true);
    setReplyError("");
    try {
      await emailsApi.sendReply(replyTarget.id, {
        subject: editedSubject,
        body: editedBody,
        send_email: true,
      });
      setShowReplyModal(false);
      setReplyTarget(null);
      setAiReply(null);
      loadInbox();
    } catch (err: any) {
      setReplyError(err.response?.data?.detail || t("inbox.error.send_reply"));
    } finally {
      setSendingReply(false);
    }
  };

  const handleQuickReply = async (item: InboxItem) => {
    if (!quickReplySubject.trim() || !quickReplyBody.trim()) return;
    setSendingQuickReply(true);
    setQuickReplyError("");
    try {
      await emailsApi.replyManual(item.id, {
        subject: quickReplySubject,
        body: quickReplyBody,
      });
      setQuickReplySubject("");
      setQuickReplyBody("");
      setQuickReplyAttachments([]);
      // Refresh conversation
      const res = await emailsApi.conversation(item.id);
      setConversation(res.data?.items || []);
      loadInbox();
    } catch (err: any) {
      setQuickReplyError(err.response?.data?.detail || t("inbox.error.send_reply"));
    } finally {
      setSendingQuickReply(false);
    }
  };

  const handleSaveDraft = async () => {
    if (!quickReplySubject.trim() || !quickReplyBody.trim()) return;
    if (!replyTarget) return;
    setSavingDraft(true);
    setDraftError("");
    try {
      await emailsApi.createDraft({
        lead_id: replyTarget.lead_id,
        subject: quickReplySubject,
        body: quickReplyBody,
      });
      setQuickReplySubject("");
      setQuickReplyBody("");
      setQuickReplyAttachments([]);
      loadInbox();
    } catch (err: any) {
      setDraftError(err.response?.data?.detail || t("inbox.error.save_draft"));
    } finally {
      setSavingDraft(false);
    }
  };

  const handleForward = async (item: InboxItem) => {
    if (!forwardEmail.trim()) return;
    setSendingForward(true);
    setForwardError("");
    try {
      await emailsApi.forward(item.id, {
        to_email: forwardEmail,
        note: forwardNote,
      });
      setForwardEmail("");
      setForwardNote("");
      setShowForward(false);
      loadInbox();
    } catch (err: any) {
      setForwardError(err.response?.data?.detail || t("inbox.error.forward"));
    } finally {
      setSendingForward(false);
    }
  };

  const sentimentIcon = (s: string) => {
    switch (s) {
      case "positive":
        return <Smile className="w-4 h-4 text-eko-green" />;
      case "negative":
        return <Frown className="w-4 h-4 text-red-400" />;
      default:
        return <Meh className="w-4 h-4 text-gold" />;
    }
  };

  const priorityBadge = (p: string) => {
    switch (p) {
      case "high":
        return "bg-red-500/10 text-red-400 border-red-500/20";
      case "medium":
        return "bg-gold/10 text-gold border-gold/20";
      default:
        return "bg-gray-500/10 text-gray-400 border-gray-500/20";
    }
  };

  const intentLabel = (i: string) => {
    const map: Record<string, string> = {
      interested: t("inbox.intent.interested"),
      needs_info: t("inbox.intent.needs_info"),
      not_interested: t("inbox.intent.not_interested"),
      out_of_office: t("inbox.intent.out_of_office"),
      forwarded: t("inbox.intent.forwarded"),
      unclear: t("inbox.intent.unclear"),
    };
    return map[i] || i;
  };

  const unreadCount = items.filter((i) => !i.read).length;

  const toggleSelect = (id: number) => {
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const toggleSelectAll = () => {
    if (selectedIds.size === items.length && items.length > 0) {
      setSelectedIds(new Set());
    } else {
      setSelectedIds(new Set(items.map((i) => i.id)));
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm(t("inbox.confirm.delete_one"))) return;
    setDeletingIds((prev) => new Set(prev).add(id));
    try {
      await emailsApi.delete(id);
      setItems((prev) => prev.filter((item) => item.id !== id));
      setSelectedIds((prev) => {
        const next = new Set(prev);
        next.delete(id);
        return next;
      });
      if (expandedId === id) setExpandedId(null);
    } catch (err) {
      console.error(err);
      alert(t("inbox.error.delete"));
    } finally {
      setDeletingIds((prev) => {
        const next = new Set(prev);
        next.delete(id);
        return next;
      });
    }
  };

  const handleBulkDelete = async () => {
    if (selectedIds.size === 0) return;
    if (!confirm(`${t("inbox.confirm.delete_many_prefix")} ${selectedIds.size} ${selectedIds.size > 1 ? t("inbox.confirm.delete_many_plural") : t("inbox.confirm.delete_many_singular")}`)) return;
    setBulkDeleting(true);
    try {
      await emailsApi.bulkDelete(Array.from(selectedIds));
      setItems((prev) => prev.filter((item) => !selectedIds.has(item.id)));
      setSelectedIds(new Set());
      setExpandedId(null);
    } catch (err) {
      console.error(err);
      alert(t("inbox.error.bulk_delete"));
    } finally {
      setBulkDeleting(false);
    }
  };

  return (
    <div className="min-h-screen bg-eko-graphite">
      <Navbar />
      <main className="pt-20 pb-12 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-eko-blue/10 text-eko-blue">
              <Inbox className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-2xl font-bold font-display">
                {folder === "inbox" ? t("inbox.header.inbox") : folder === "sent" ? t("inbox.header.sent") : t("inbox.header.all")}
              </h1>
              <p className="text-gray-400 text-sm">
                {unreadCount > 0
                  ? `${unreadCount} ${unreadCount > 1 ? t("inbox.header.unread_plural") : t("inbox.header.unread_singular")}`
                  : t("inbox.header.no_new")}
              </p>
            </div>
          </div>
          <button
            onClick={handleSimulateReply}
            disabled={simulating}
            className="flex items-center gap-2 rounded-lg border border-white/10 px-4 py-2 text-sm text-gray-300 hover:bg-white/5 transition-colors disabled:opacity-50"
          >
            {simulating ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
            {t("inbox.action.simulate_reply")}
          </button>
        </div>

        {/* Bulk actions bar */}
        {selectedIds.size > 0 && (
          <div className="flex items-center justify-between mb-4 p-3 bg-red-500/5 border border-red-500/20 rounded-lg">
            <span className="text-sm text-gray-300">
              {selectedIds.size} {selectedIds.size > 1 ? t("inbox.bulk.selected_plural") : t("inbox.bulk.selected_singular")}
            </span>
            <button
              onClick={handleBulkDelete}
              disabled={bulkDeleting}
              className="flex items-center gap-2 px-3 py-1.5 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 text-sm"
            >
              {bulkDeleting ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Trash2 className="w-4 h-4" />
              )}
              {t("common.delete")}
            </button>
          </div>
        )}

        {/* Folder tabs */}
        <div className="flex items-center gap-1 bg-white/5 rounded-lg p-1 mb-4 w-fit">
          {(["inbox", "sent", "drafts", "all"] as const).map((f) => (
            <button
              key={f}
              onClick={() => setFolder(f)}
              className={`px-3 py-1.5 rounded-md text-sm capitalize transition-colors ${
                folder === f
                  ? "bg-white/10 text-white"
                  : "text-gray-400 hover:text-white"
              }`}
            >
              {f === "inbox" ? t("inbox.folder.inbox") : f === "sent" ? t("inbox.folder.sent") : f === "drafts" ? t("inbox.folder.drafts") : t("inbox.folder.all")}
            </button>
          ))}
        </div>

        {/* Filters */}
        <div className="flex items-center gap-1 bg-white/5 rounded-lg p-1 mb-6 w-fit">
          {(["all", "unread", "high_priority"] as const).map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-3 py-1.5 rounded-md text-sm capitalize transition-colors ${
                filter === f
                  ? "bg-white/10 text-white"
                  : "text-gray-400 hover:text-white"
              }`}
            >
              {f === "high_priority" ? t("inbox.filter.high_priority") : f === "unread" ? t("inbox.filter.unread") : t("inbox.filter.all")}
            </button>
          ))}
        </div>

        {/* List */}
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="w-8 h-8 animate-spin text-eko-blue" />
          </div>
        ) : items.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 text-gray-500">
            <MailOpen className="w-12 h-12 mb-4 opacity-50" />
            <p className="text-lg font-medium">
              {folder === "drafts" ? t("inbox.empty.drafts_title") : t("inbox.empty.inbox_title")}
            </p>
            <p className="text-sm mt-1">
              {filter === "unread"
                ? t("inbox.empty.no_unread")
                : filter === "high_priority"
                ? t("inbox.empty.no_high_priority")
                : folder === "sent"
                ? t("inbox.empty.no_sent")
                : folder === "drafts"
                ? t("inbox.empty.no_drafts")
                : folder === "all"
                ? t("inbox.empty.no_emails")
                : t("inbox.empty.emails_will_appear")}
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {items.map((item) => {
              const isExpanded = expandedId === item.id;
              return (
                <div
                  key={item.id}
                  className={`rounded-xl border transition-colors ${
                    item.read
                      ? "border-white/5 bg-white/[0.02]"
                      : "border-eko-blue/20 bg-eko-blue/[0.02]"
                  }`}
                >
                  {/* Header row */}
                  <div
                    className="p-4 cursor-pointer"
                    onClick={async () => {
                      const nextExpanded = isExpanded ? null : item.id;
                      setExpandedId(nextExpanded);
                      if (nextExpanded) {
                        setLoadingConversation(true);
                        try {
                          const res = await emailsApi.conversation(item.id);
                          setConversation(res.data?.items || []);
                        } catch (err) {
                          console.error(err);
                        } finally {
                          setLoadingConversation(false);
                        }
                      }
                    }}
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1 flex-wrap">
                          <input
                            type="checkbox"
                            checked={selectedIds.has(item.id)}
                            onClick={(e) => e.stopPropagation()}
                            onChange={() => toggleSelect(item.id)}
                            className="w-4 h-4 rounded border-white/20 bg-white/5 text-eko-blue focus:ring-eko-blue cursor-pointer"
                          />
                          {!item.read && (
                            <span className="w-2 h-2 rounded-full bg-eko-blue" />
                          )}
                          <span className="font-medium text-sm truncate">
                            {item.lead_name}
                          </span>
                          <span className="text-xs text-gray-500">
                            {item.lead_email}
                          </span>
                          {(item.lead_total_count || 0) > 1 && (
                            <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-white/10 text-gray-400">
                              {item.lead_total_count} {t("inbox.thread.messages")}
                              {(item.lead_unread_count || 0) > 0 && (
                                <span className="ml-1 text-eko-blue">({item.lead_unread_count} {t("inbox.thread.unread_lower")})</span>
                              )}
                            </span>
                          )}
                          <span className={`text-[10px] px-1.5 py-0.5 rounded border ${
                            item.direction === "outbound"
                              ? "bg-purple-500/10 text-purple-400 border-purple-500/20"
                              : "bg-eko-blue/10 text-eko-blue border-eko-blue/20"
                          }`}>
                            {item.direction === "outbound" ? t("inbox.direction.last_sent") : t("inbox.direction.last_received")}
                          </span>
                          {item.auto_status_changed && (
                            <span className="text-[10px] px-1.5 py-0.5 rounded bg-eko-green/10 text-eko-green border border-eko-green/20">
                              {t("inbox.badge.status_auto_updated")}
                            </span>
                          )}
                        </div>
                        <p className="text-sm text-gray-300 truncate">
                          {item.subject || t("inbox.no_subject")}
                        </p>
                        <p className="text-xs text-gray-500 truncate">
                          {stripHtml(item.content).substring(0, 120)}
                        </p>
                        <div className="flex items-center gap-3 mt-2 flex-wrap">
                          <span
                            className={`flex items-center gap-1 text-xs px-2 py-0.5 rounded-full border ${priorityBadge(
                              item.priority
                            )}`}
                          >
                            {item.priority}
                          </span>
                          <span className="flex items-center gap-1 text-xs text-gray-400">
                            {sentimentIcon(item.sentiment)}
                            {item.sentiment}
                          </span>
                          <span className="text-xs text-gray-500 capitalize">
                            {intentLabel(item.intent)}
                          </span>
                          <span className="text-xs text-gray-500 flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            {new Date(item.created_at).toLocaleString("es-ES", {
                              day: "numeric",
                              month: "short",
                              hour: "2-digit",
                              minute: "2-digit",
                            })}
                          </span>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleDelete(item.id);
                          }}
                          disabled={deletingIds.has(item.id)}
                          className="p-1.5 rounded-lg text-gray-400 hover:text-red-400 hover:bg-red-500/10 transition-colors"
                          title={t("common.delete")}
                        >
                          {deletingIds.has(item.id) ? (
                            <Loader2 className="w-4 h-4 animate-spin" />
                          ) : (
                            <Trash2 className="w-4 h-4" />
                          )}
                        </button>
                        {!item.read && (
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleMarkRead(item.id);
                            }}
                            disabled={markingRead === item.id}
                            className="p-1.5 rounded-lg text-gray-400 hover:text-eko-blue hover:bg-eko-blue/10 transition-colors"
                            title={t("inbox.action.mark_read")}
                          >
                            {markingRead === item.id ? (
                              <Loader2 className="w-4 h-4 animate-spin" />
                            ) : (
                              <MailOpen className="w-4 h-4" />
                            )}
                          </button>
                        )}
                        {isExpanded ? (
                          <ChevronUp className="w-4 h-4 text-gray-500" />
                        ) : (
                          <ChevronDown className="w-4 h-4 text-gray-500" />
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Expanded content — Thread View */}
                  {isExpanded && (
                    <div className="px-4 pb-4 border-t border-white/5 pt-3">
                      {/* AI Summary (only for inbound) */}
                      {item.direction === "inbound" && item.summary && (
                        <div className="mb-3 rounded-lg bg-white/5 p-3">
                          <div className="flex items-center gap-2 mb-1">
                            <Zap className="w-3.5 h-3.5 text-eko-blue" />
                            <span className="text-xs font-medium text-eko-blue">
                              {t("inbox.ai_summary")}
                            </span>
                          </div>
                          <p className="text-sm text-gray-300">{item.summary}</p>
                        </div>
                      )}

                      {/* Thread / Conversation */}
                      <div className="mb-4">
                        <p className="text-xs text-gray-500 font-medium mb-2">{t("inbox.thread.title")}</p>
                        {loadingConversation ? (
                          <div className="flex items-center justify-center py-4">
                            <Loader2 className="w-5 h-5 animate-spin text-gray-400" />
                          </div>
                        ) : conversation.length > 0 ? (
                          <div className="space-y-3 max-h-80 overflow-y-auto pr-1">
                            {conversation.map((msg) => (
                              <div
                                key={msg.id}
                                className={`flex ${
                                  msg.direction === "outbound" ? "justify-end" : "justify-start"
                                }`}
                              >
                                <div
                                  className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm ${
                                    msg.direction === "outbound"
                                      ? "bg-purple-600/20 border border-purple-500/30 text-gray-200 rounded-br-md"
                                      : "bg-white/5 border border-white/10 text-gray-300 rounded-bl-md"
                                  }`}
                                >
                                  <div className="flex items-center gap-2 mb-1">
                                    <span className="text-[10px] font-medium uppercase tracking-wider text-gray-500">
                                      {msg.direction === "outbound" ? t("inbox.thread.us") : t("inbox.thread.client")}
                                    </span>
                                    <span className="text-[10px] text-gray-600">
                                      {new Date(msg.created_at).toLocaleString("es-ES", {
                                        day: "numeric",
                                        month: "short",
                                        hour: "2-digit",
                                        minute: "2-digit",
                                      })}
                                    </span>
                                  </div>
                                  <p className="font-medium text-xs mb-1 opacity-80">{msg.subject || t("inbox.no_subject")}</p>
                                  <div
                                    className="whitespace-pre-wrap prose prose-invert prose-sm max-w-none"
                                    dangerouslySetInnerHTML={{ __html: msg.content }}
                                  />
                                </div>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <p className="text-sm text-gray-500 italic">{t("inbox.thread.empty")}</p>
                        )}
                      </div>

                      {/* Forward section */}
                      {showForward && item.direction === "inbound" && (
                        <div className="mb-4 rounded-lg bg-white/[0.03] border border-white/10 p-3">
                          <p className="text-xs text-gray-500 font-medium mb-2">{t("inbox.forward.title")}</p>
                          {forwardError && (
                            <div className="p-2 mb-2 bg-red-500/10 border border-red-500/20 rounded text-red-400 text-xs">
                              {forwardError}
                            </div>
                          )}
                          <input
                            type="email"
                            placeholder={t("inbox.forward.email_placeholder")}
                            value={forwardEmail}
                            onChange={(e) => setForwardEmail(e.target.value)}
                            className="w-full px-3 py-2 mb-2 bg-white/5 border border-white/10 rounded-lg text-sm text-white focus:ring-2 focus:ring-eko-blue placeholder-gray-600"
                          />
                          <textarea
                            placeholder={t("inbox.forward.note_placeholder")}
                            value={forwardNote}
                            onChange={(e) => setForwardNote(e.target.value)}
                            rows={2}
                            className="w-full px-3 py-2 mb-2 bg-white/5 border border-white/10 rounded-lg text-sm text-white focus:ring-2 focus:ring-eko-blue resize-none placeholder-gray-600"
                          />
                          <div className="flex items-center gap-2">
                            <button
                              onClick={() => handleForward(item)}
                              disabled={sendingForward || !forwardEmail.trim()}
                              className="flex items-center gap-2 px-4 py-2 bg-eko-blue text-white rounded-lg hover:bg-eko-blue/80 transition-colors disabled:opacity-50 text-sm"
                            >
                              {sendingForward ? (
                                <Loader2 className="w-4 h-4 animate-spin" />
                              ) : (
                                <Send className="w-4 h-4" />
                              )}
                              {t("inbox.forward.send")}
                            </button>
                            <button
                              onClick={() => { setShowForward(false); setForwardEmail(""); setForwardNote(""); }}
                              className="px-4 py-2 border border-white/10 text-gray-300 rounded-lg hover:bg-white/5 transition-colors text-sm"
                            >
                              {t("common.cancel")}
                            </button>
                          </div>
                        </div>
                      )}

                      {/* Quick Manual Reply */}
                      {item.direction === "inbound" && (
                        <div className="mb-4 rounded-lg bg-white/[0.03] border border-white/10 p-3">
                          <p className="text-xs text-gray-500 font-medium mb-2">{t("inbox.quick_reply.title")}</p>
                          {quickReplyError && (
                            <div className="p-2 mb-2 bg-red-500/10 border border-red-500/20 rounded text-red-400 text-xs">
                              {quickReplyError}
                            </div>
                          )}
                          {draftError && (
                            <div className="p-2 mb-2 bg-yellow-500/10 border border-yellow-500/20 rounded text-yellow-400 text-xs">
                              {draftError}
                            </div>
                          )}
                          <input
                            type="text"
                            placeholder={t("inbox.field.subject")}
                            value={quickReplySubject}
                            onChange={(e) => setQuickReplySubject(e.target.value)}
                            className="w-full px-3 py-2 mb-2 bg-white/5 border border-white/10 rounded-lg text-sm text-white focus:ring-2 focus:ring-eko-blue placeholder-gray-600"
                          />
                          <textarea
                            placeholder={t("inbox.quick_reply.body_placeholder")}
                            value={quickReplyBody}
                            onChange={(e) => setQuickReplyBody(e.target.value)}
                            rows={3}
                            className="w-full px-3 py-2 mb-2 bg-white/5 border border-white/10 rounded-lg text-sm text-white focus:ring-2 focus:ring-eko-blue resize-none placeholder-gray-600"
                          />
                          {/* File attachment input */}
                          <div className="mb-2">
                            <label className="flex items-center gap-2 px-3 py-2 bg-white/5 border border-white/10 border-dashed rounded-lg text-sm text-gray-400 hover:bg-white/[0.07] hover:text-gray-300 transition-colors cursor-pointer">
                              <Edit3 className="w-4 h-4" />
                              {quickReplyAttachments.length > 0
                                ? `${quickReplyAttachments.length} ${t("inbox.attachment.files_selected")}`
                                : t("inbox.attachment.attach")}
                              <input
                                type="file"
                                multiple
                                className="hidden"
                                onChange={(e) => {
                                  const files = Array.from(e.target.files || []);
                                  if (files.length > 0) {
                                    setQuickReplyAttachments((prev) => [...prev, ...files]);
                                  }
                                }}
                              />
                            </label>
                            {quickReplyAttachments.length > 0 && (
                              <div className="mt-1 flex flex-wrap gap-1">
                                {quickReplyAttachments.map((file, idx) => (
                                  <span
                                    key={idx}
                                    className="inline-flex items-center gap-1 px-2 py-0.5 bg-white/5 rounded text-xs text-gray-400"
                                  >
                                    {file.name}
                                    <button
                                      onClick={() =>
                                        setQuickReplyAttachments((prev) => prev.filter((_, i) => i !== idx))
                                      }
                                      className="text-gray-500 hover:text-red-400"
                                    >
                                      ×
                                    </button>
                                  </span>
                                ))}
                              </div>
                            )}
                          </div>
                          <div className="flex items-center gap-2 flex-wrap">
                            <button
                              onClick={() => handleQuickReply(item)}
                              disabled={sendingQuickReply || !quickReplySubject.trim() || !quickReplyBody.trim()}
                              className="flex items-center gap-2 px-4 py-2 bg-eko-blue text-white rounded-lg hover:bg-eko-blue/80 transition-colors disabled:opacity-50 text-sm"
                            >
                              {sendingQuickReply ? (
                                <Loader2 className="w-4 h-4 animate-spin" />
                              ) : (
                                <Send className="w-4 h-4" />
                              )}
                              {t("inbox.action.send_reply")}
                            </button>
                            <button
                              onClick={handleSaveDraft}
                              disabled={savingDraft || !quickReplySubject.trim() || !quickReplyBody.trim()}
                              className="flex items-center gap-2 px-4 py-2 border border-white/10 text-gray-300 rounded-lg hover:bg-white/5 transition-colors disabled:opacity-50 text-sm"
                            >
                              {savingDraft ? (
                                <Loader2 className="w-4 h-4 animate-spin" />
                              ) : (
                                <Edit3 className="w-4 h-4" />
                              )}
                              {t("inbox.action.save_draft")}
                            </button>
                          </div>
                        </div>
                      )}

                      {/* Action buttons */}
                      <div className="flex items-center gap-2">
                        {item.direction === "inbound" && (
                          <>
                            <button
                              onClick={() => openReplyModal(item)}
                              className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-sm"
                            >
                              <Wand2 className="w-4 h-4" />
                              {t("inbox.action.reply_ai")}
                            </button>
                            <button
                              onClick={() => { setShowForward(true); setReplyTarget(item); }}
                              className="flex items-center gap-2 px-4 py-2 border border-white/10 text-gray-300 rounded-lg hover:bg-white/5 transition-colors text-sm"
                            >
                              <ArrowLeft className="w-4 h-4" />
                              {t("inbox.action.forward")}
                            </button>
                          </>
                        )}
                        <button
                          onClick={() => handleDelete(item.id)}
                          disabled={deletingIds.has(item.id)}
                          className="flex items-center gap-2 px-4 py-2 border border-red-500/30 text-red-400 rounded-lg hover:bg-red-500/10 transition-colors text-sm"
                        >
                          {deletingIds.has(item.id) ? (
                            <Loader2 className="w-4 h-4 animate-spin" />
                          ) : (
                            <Trash2 className="w-4 h-4" />
                          )}
                          {t("common.delete")}
                        </button>
                      </div>

                      {/* Status change info */}
                      {item.auto_status_changed && (
                        <div className="mt-3 text-xs text-gray-500">
                          {t("inbox.status_changed_prefix")}: {item.previous_status} → {item.lead_status}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </main>

      {/* AI Reply Modal */}
      {showReplyModal && replyTarget && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-black/60" onClick={() => setShowReplyModal(false)} />
          <div className="relative bg-eko-graphite border border-white/10 rounded-xl w-full max-w-3xl max-h-[90vh] overflow-hidden flex flex-col">
            {/* Modal header */}
            <div className="flex items-center justify-between p-4 border-b border-white/10">
              <div className="flex items-center gap-3">
                <MessageSquare className="w-5 h-5 text-purple-400" />
                <div>
                  <h3 className="font-semibold text-white">{t("inbox.modal.reply_to")} {replyTarget.lead_name}</h3>
                  <p className="text-xs text-gray-400">{replyTarget.subject}</p>
                </div>
              </div>
              <button
                onClick={() => setShowReplyModal(false)}
                className="p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal body */}
            <div className="flex-1 overflow-auto p-4 space-y-4">
              {/* Error */}
              {replyError && (
                <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400 text-sm">
                  {replyError}
                </div>
              )}

              {/* Conversation preview */}
              {loadingConversation ? (
                <div className="flex items-center justify-center py-4">
                  <Loader2 className="w-5 h-5 animate-spin text-gray-400" />
                </div>
              ) : conversation.length > 0 ? (
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  <p className="text-xs text-gray-500 font-medium">{t("inbox.modal.previous_conversation")}</p>
                  {conversation.slice(0, 5).map((msg) => (
                    <div
                      key={msg.id}
                      className={`p-2 rounded-lg text-sm ${
                        msg.direction === "outbound"
                          ? "bg-purple-500/10 border border-purple-500/20 ml-4"
                          : "bg-white/5 border border-white/10 mr-4"
                      }`}
                    >
                      <p className="text-xs text-gray-500 mb-0.5">
                        {msg.direction === "outbound" ? t("inbox.thread.us") : t("inbox.thread.client")}
                      </p>
                      <p className="text-gray-300 line-clamp-2">{msg.content}</p>
                    </div>
                  ))}
                </div>
              ) : null}

              {/* Tone and length selectors */}
              {!aiReply && (
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs text-gray-500 mb-1">{t("inbox.modal.tone")}</label>
                    <select
                      value={replyTone}
                      onChange={(e) => setReplyTone(e.target.value)}
                      className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-sm text-white focus:ring-2 focus:ring-purple-500"
                    >
                      <option value="professional">{t("inbox.tone.professional")}</option>
                      <option value="friendly">{t("inbox.tone.friendly")}</option>
                      <option value="assertive">{t("inbox.tone.assertive")}</option>
                      <option value="consultative">{t("inbox.tone.consultative")}</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs text-gray-500 mb-1">{t("inbox.modal.length")}</label>
                    <select
                      value={replyLength}
                      onChange={(e) => setReplyLength(e.target.value)}
                      className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-sm text-white focus:ring-2 focus:ring-purple-500"
                    >
                      <option value="short">{t("inbox.length.short")}</option>
                      <option value="medium">{t("inbox.length.medium")}</option>
                      <option value="long">{t("inbox.length.long")}</option>
                    </select>
                  </div>
                </div>
              )}

              {/* Generate button */}
              {!aiReply && (
                <button
                  onClick={handleGenerateReply}
                  disabled={generatingReply}
                  className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50"
                >
                  {generatingReply ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <Wand2 className="w-5 h-5" />
                  )}
                  {generatingReply ? t("inbox.modal.generating") : t("inbox.modal.generate_ai")}
                </button>
              )}

              {/* Generated reply editor */}
              {aiReply && (
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <Zap className="w-4 h-4 text-purple-400" />
                    <span className="text-sm text-purple-400 font-medium">
                      {t("inbox.modal.generated_reply")} ({Math.round(aiReply.confidence * 100)}% {t("inbox.modal.confidence")})
                    </span>
                    {aiReply.suggested_next_action && (
                      <span className="text-xs text-gray-500 ml-auto">
                        {t("inbox.modal.next_step")}: {aiReply.suggested_next_action}
                      </span>
                    )}
                  </div>

                  <div>
                    <label className="block text-xs text-gray-500 mb-1">{t("inbox.field.subject")}</label>
                    <div className="flex items-center gap-2">
                      <input
                        type="text"
                        value={editedSubject}
                        onChange={(e) => setEditedSubject(e.target.value)}
                        className="flex-1 px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-sm text-white focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs text-gray-500 mb-1">{t("inbox.field.message")}</label>
                    <textarea
                      value={editedBody}
                      onChange={(e) => setEditedBody(e.target.value)}
                      rows={12}
                      className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-sm text-white focus:ring-2 focus:ring-purple-500 resize-none"
                    />
                  </div>

                  <div className="flex items-center gap-3">
                    <button
                      onClick={handleSendReply}
                      disabled={sendingReply || !editedSubject || !editedBody}
                      className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
                    >
                      {sendingReply ? (
                        <Loader2 className="w-4 h-4 animate-spin" />
                      ) : (
                        <Send className="w-4 h-4" />
                      )}
                      {sendingReply ? t("inbox.action.sending") : t("inbox.action.send_reply")}
                    </button>
                    <button
                      onClick={() => {
                        setAiReply(null);
                        setEditedSubject("");
                        setEditedBody("");
                      }}
                      className="px-4 py-2 border border-white/10 text-gray-300 rounded-lg hover:bg-white/5 transition-colors text-sm"
                    >
                      {t("inbox.action.regenerate")}
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
