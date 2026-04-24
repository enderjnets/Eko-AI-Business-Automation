"use client";

import { useState } from "react";
import { Send, Loader2, Sparkles, X } from "lucide-react";
import { crmApi } from "@/lib/api";

interface EmailComposerProps {
  leadId: number;
  leadName: string;
  leadEmail?: string;
  onClose?: () => void;
  onSent?: () => void;
}

export default function EmailComposer({ leadId, leadName, leadEmail, onClose, onSent }: EmailComposerProps) {
  const [mode, setMode] = useState<"ai" | "manual">("ai");
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [campaignContext, setCampaignContext] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  const handleSendAI = async () => {
    if (!leadEmail) {
      setError("Lead has no email address");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const res = await crmApi.contact(leadId, "email", "initial_outreach", undefined, undefined);
      setResult(res.data);
      onSent?.();
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to send email");
    } finally {
      setLoading(false);
    }
  };

  const handleSendManual = async () => {
    if (!subject.trim() || !body.trim()) {
      setError("Subject and body are required");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const res = await crmApi.contact(leadId, "email", undefined, subject, body);
      setResult(res.data);
      onSent?.();
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to send email");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="rounded-xl border border-white/5 bg-white/[0.02] p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-medium">Send Email to {leadName}</h3>
        {onClose && (
          <button onClick={onClose} className="text-gray-500 hover:text-white">
            <X className="w-4 h-4" />
          </button>
        )}
      </div>

      {!leadEmail && (
        <div className="rounded-lg bg-red-500/10 border border-red-500/20 p-3 mb-4">
          <p className="text-sm text-red-400">This lead has no email address.</p>
        </div>
      )}

      {/* Mode toggle */}
      <div className="flex gap-2 mb-4">
        <button
          onClick={() => setMode("ai")}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm transition-colors ${
            mode === "ai" ? "bg-eko-blue text-white" : "bg-white/5 text-gray-400 hover:bg-white/10"
          }`}
        >
          <Sparkles className="w-3.5 h-3.5" />
          AI Generated
        </button>
        <button
          onClick={() => setMode("manual")}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm transition-colors ${
            mode === "manual" ? "bg-eko-blue text-white" : "bg-white/5 text-gray-400 hover:bg-white/10"
          }`}
        >
          Manual
        </button>
      </div>

      {mode === "ai" ? (
        <div className="space-y-3">
          <div>
            <label className="block text-xs text-gray-400 mb-1">Campaign Context (optional)</label>
            <textarea
              value={campaignContext}
              onChange={(e) => setCampaignContext(e.target.value)}
              placeholder="Any specific context for the AI..."
              rows={2}
              className="w-full rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm focus:border-eko-blue focus:outline-none resize-none"
            />
          </div>
          
          <button
            onClick={handleSendAI}
            disabled={loading || !leadEmail}
            className="w-full flex items-center justify-center gap-2 rounded-lg bg-eko-blue px-4 py-2.5 text-sm font-medium hover:bg-eko-blue-dark disabled:opacity-50 transition-colors"
          >
            {loading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Sparkles className="w-4 h-4" />
            )}
            Generate & Send with AI
          </button>
        </div>
      ) : (
        <div className="space-y-3">
          <div>
            <label className="block text-xs text-gray-400 mb-1">Subject</label>
            <input
              type="text"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              placeholder="Email subject..."
              className="w-full rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm focus:border-eko-blue focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-xs text-gray-400 mb-1">Body (HTML)</label>
            <textarea
              value={body}
              onChange={(e) => setBody(e.target.value)}
              placeholder="<p>Your email content...</p>"
              rows={6}
              className="w-full rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm focus:border-eko-blue focus:outline-none resize-none font-mono"
            />
          </div>
          
          <button
            onClick={handleSendManual}
            disabled={loading || !leadEmail}
            className="w-full flex items-center justify-center gap-2 rounded-lg bg-white/10 px-4 py-2.5 text-sm font-medium hover:bg-white/15 disabled:opacity-50 transition-colors"
          >
            {loading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
            Send Manual Email
          </button>
        </div>
      )}

      {error && (
        <p className="mt-3 text-sm text-red-400">{error}</p>
      )}

      {result && (
        <div className="mt-3 rounded-lg bg-eko-green/10 border border-eko-green/20 p-3">
          <p className="text-sm text-eko-green">
            ✓ Email sent! Message ID: {result.message_id}
          </p>
        </div>
      )}
    </div>
  );
}
