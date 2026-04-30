"use client";

import { useState, useEffect } from "react";
import { Calendar, Clock, CheckCircle, Loader2, User, Mail, MessageSquare } from "lucide-react";

export default function BookDemoForm() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    date: "",
    time: "",
    message: "",
  });

  useEffect(() => {
    if (typeof window !== "undefined") {
      const params = new URLSearchParams(window.location.search);
      const prefillEmail = params.get("email") || "";
      const prefillName = params.get("name") || "";
      setForm(prev => ({
        ...prev,
        name: prefillName,
        email: prefillEmail,
      }));
    }
  }, []);
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const timeSlots = [
    "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
    "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30",
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await fetch("/api/v1/calendar/book-demo", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      setSubmitted(true);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <div className="min-h-screen bg-eko-graphite flex items-center justify-center p-4">
        <div className="max-w-md w-full text-center">
          <CheckCircle className="w-16 h-16 text-green-400 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-white mb-2">Demo Scheduled!</h1>
          <p className="text-gray-400 mb-6">
            Thank you {form.name || ""}. We&apos;ll contact you soon to confirm your demo on {form.date} at {form.time} (MT).
          </p>
          <a href="/" className="text-eko-blue hover:underline">
            Back to home
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-eko-graphite flex items-center justify-center p-4">
      <div className="max-w-lg w-full">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Book a Demo</h1>
          <p className="text-gray-400">15 minutes to see how Eko AI transforms your business</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm text-gray-400 mb-1.5">Business name</label>
            <div className="relative">
              <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
              <input
                type="text"
                required
                value={form.name}
                onChange={(e: any) => setForm({ ...form, name: e.target.value })}
                className="w-full bg-white/5 border border-white/10 rounded-lg pl-10 pr-4 py-2.5 text-white placeholder-gray-500 focus:outline-none focus:border-eko-blue"
                placeholder="e.g. The Pampering Place"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm text-gray-400 mb-1.5">Email</label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
              <input
                type="email"
                required
                value={form.email}
                onChange={(e: any) => setForm({ ...form, email: e.target.value })}
                className="w-full bg-white/5 border border-white/10 rounded-lg pl-10 pr-4 py-2.5 text-white placeholder-gray-500 focus:outline-none focus:border-eko-blue"
                placeholder="you@email.com"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm text-gray-400 mb-1.5">Preferred date</label>
            <div className="relative">
              <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
              <input
                type="date"
                required
                min={new Date().toISOString().split("T")[0]}
                value={form.date}
                onChange={(e: any) => setForm({ ...form, date: e.target.value })}
                className="w-full bg-white/5 border border-white/10 rounded-lg pl-10 pr-4 py-2.5 text-white placeholder-gray-500 focus:outline-none focus:border-eko-blue"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm text-gray-400 mb-1.5">Preferred time (MT)</label>
            <div className="grid grid-cols-4 gap-2">
              {timeSlots.map((t: string) => (
                <button
                  key={t}
                  type="button"
                  onClick={() => setForm({ ...form, time: t })}
                  className={`py-2 rounded-lg text-sm border transition-colors ${
                    form.time === t
                      ? "bg-eko-blue border-eko-blue text-white"
                      : "bg-white/5 border-white/10 text-gray-300 hover:border-white/30"
                  }`}
                >
                  {t}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm text-gray-400 mb-1.5">Message (optional)</label>
            <div className="relative">
              <MessageSquare className="absolute left-3 top-3 w-4 h-4 text-gray-500" />
              <textarea
                value={form.message}
                onChange={(e: any) => setForm({ ...form, message: e.target.value })}
                rows={3}
                className="w-full bg-white/5 border border-white/10 rounded-lg pl-10 pr-4 py-2.5 text-white placeholder-gray-500 focus:outline-none focus:border-eko-blue resize-none"
                placeholder="Is there something specific you'd like to see?"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading || !form.time}
            className="w-full py-3 rounded-lg bg-eko-blue text-white font-semibold hover:bg-eko-blue-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Scheduling...
              </>
            ) : (
              <>
                <Clock className="w-4 h-4" />
                Book Demo
              </>
            )}
          </button>
        </form>

        <p className="text-center text-gray-500 text-sm mt-6">
          Eko AI — Denver, CO — contact@biz.ekoaiautomation.com
        </p>
      </div>
    </div>
  );
}
