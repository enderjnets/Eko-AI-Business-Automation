"use client";

import { useState, useEffect, useRef, type FormEvent, type ChangeEvent } from "react";
import Image from "next/image";
import Link from "next/link";
import {
  Zap,
  Sparkles,
  Phone,
  MessageSquare,
  Calendar,
  Mail,
  TrendingUp,
  Shield,
  CheckCircle,
  Lock,
  ChevronDown,
  ArrowRight,
  Loader2,
  Sparkle,
  UtensilsCrossed,
  Stethoscope,
  Dumbbell,
  Store,
  Briefcase,
  X,
} from "lucide-react";

/* ──────────────────────── Animation Hook ──────────────────────── */
function useScrollAnimation(threshold = 0.15) {
  const ref = useRef<HTMLDivElement>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.unobserve(el);
        }
      },
      { threshold }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, [threshold]);

  return { ref, isVisible };
}

/* ──────────────────────── Stat Counter ──────────────────────── */
function useCountUp(end: number, duration = 1500, isVisible = false) {
  const [count, setCount] = useState(0);
  const hasRun = useRef(false);

  useEffect(() => {
    if (!isVisible || hasRun.current) return;
    hasRun.current = true;
    const start = performance.now();
    const tick = (now: number) => {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 4);
      setCount(Math.floor(eased * end));
      if (progress < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }, [isVisible, end, duration]);

  return count;
}

/* ──────────────────────── Data ──────────────────────── */
const INDUSTRIES = [
  { icon: Sparkle, label: "Spas & Salons" },
  { icon: UtensilsCrossed, label: "Restaurants" },
  { icon: Stethoscope, label: "Clinics" },
  { icon: Dumbbell, label: "Gyms" },
  { icon: Store, label: "Retail" },
  { icon: Briefcase, label: "Professionals" },
];

const FEATURES = [
  { icon: Phone, title: "Answer Calls 24/7", desc: "Never miss a call again. Your AI answers, qualifies leads, and transfers when needed." },
  { icon: MessageSquare, title: "Respond on WhatsApp", desc: "Instant replies to customer inquiries. Product questions, pricing, availability — all automatic." },
  { icon: Calendar, title: "Book Appointments", desc: "Connects directly to your calendar. Customers book, reschedule, or cancel without human help." },
  { icon: Mail, title: "Handle Email", desc: "Responds to customer emails within seconds. Professional, on-brand, always accurate." },
  { icon: TrendingUp, title: "Follow Up with Leads", desc: "Automatically nurtures leads with personalized follow-ups. No lead falls through the cracks." },
  { icon: Shield, title: "Secure & Compliant", desc: "Enterprise-grade security. Customer data protected. Full privacy compliance." },
];

const HOW_STEPS = [
  { step: "01", title: "Book Your Demo", desc: "15 minutes. We learn about your business and show you exactly how AI will work for you. No pressure." },
  { step: "02", title: "We Configure Everything", desc: "Our team trains your AI agent with your business info, services, pricing, and brand voice." },
  { step: "03", title: "Go Live & Scale", desc: "Your AI starts working immediately. Answer calls, book appointments, follow up — 24/7 from day one." },
];

const FAQS = [
  { q: "How quickly can Eko AI be set up?", a: "Most businesses are live within 48 hours of their demo. We handle all the configuration, training, and integration. You just approve the setup." },
  { q: "Does it work with my existing tools?", a: "Yes. Eko AI integrates with Google Calendar, Outlook, Cal.com, most CRMs, and popular business phone systems." },
  { q: "What if the AI can't answer a question?", a: "Your AI is trained specifically on your business. For edge cases, it can transfer to you or take a message with full context." },
  { q: "Is my customer data secure?", a: "Absolutely. We use enterprise-grade encryption and are fully compliant with data privacy regulations. Your data is never shared or sold." },
  { q: "Can I cancel anytime?", a: "Yes. No long-term contracts, no cancellation fees. We earn your business every month." },
];

const STATS = [
  { value: 500, suffix: "+", label: "Businesses automated" },
  { value: 50000, suffix: "+", label: "Interactions monthly" },
  { value: 18, suffix: " hrs", label: "Weekly hours saved" },
  { value: 80, suffix: "%", label: "Faster responses" },
];

/* ──────────────────────── Animated Section ──────────────────────── */
function AnimatedSection({ children, className = "", delay = 0 }: { children: React.ReactNode; className?: string; delay?: number }) {
  const { ref, isVisible } = useScrollAnimation();
  return (
    <div
      ref={ref}
      className={className}
      style={{
        opacity: isVisible ? 1 : 0,
        transform: isVisible ? "translateY(0)" : "translateY(30px)",
        transition: `opacity 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94) ${delay}s, transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94) ${delay}s`,
      }}
    >
      {children}
    </div>
  );
}

/* ──────────────────────── FAQ Item ──────────────────────── */
function FAQItem({ item, isOpen, onToggle }: { item: typeof FAQS[0]; isOpen: boolean; onToggle: () => void }) {
  return (
    <div className="border-b border-[#334155]">
      <button
        onClick={onToggle}
        className="w-full flex items-center justify-between py-5 text-left group"
      >
        <span className="text-lg text-[#F8FAFC] font-medium pr-4 group-hover:text-[#0B4FD8] transition-colors text-left">
          {item.q}
        </span>
        <ChevronDown
          className="w-5 h-5 text-[#64748B] flex-shrink-0 transition-transform duration-300"
          style={{ transform: isOpen ? "rotate(180deg)" : "rotate(0deg)" }}
        />
      </button>
      <div
        className="overflow-hidden transition-all duration-300 ease-out"
        style={{ maxHeight: isOpen ? "300px" : "0", opacity: isOpen ? 1 : 0 }}
      >
        <p className="pb-5 text-[#CBD5E1] leading-relaxed">{item.a}</p>
      </div>
    </div>
  );
}

/* ──────────────────────── Success Modal ──────────────────────── */
function SuccessModal({ open, onClose, name }: { open: boolean; onClose: () => void; name: string }) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" />
      <div
        className="relative bg-[#1E293B] border border-[#334155] rounded-2xl p-8 max-w-md w-full text-center"
        onClick={(e) => e.stopPropagation()}
      >
        <button onClick={onClose} className="absolute top-4 right-4 text-[#64748B] hover:text-white transition-colors">
          <X className="w-5 h-5" />
        </button>
        <CheckCircle className="w-16 h-16 text-[#10B981] mx-auto mb-4" />
        <h3 className="text-2xl font-bold text-white mb-3">Thank you, {name}!</h3>
        <p className="text-[#CBD5E1] mb-6 leading-relaxed">
          We&apos;ve received your information. Our team will analyze your business and send your personalized AI automation report within 24 hours.
        </p>
        <a
          href="https://cal.com/ender-ocando-lfxtkn/15min"
          target="_blank"
          rel="noopener noreferrer"
          onClick={onClose}
          className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-[#0B4FD8] text-white font-semibold hover:bg-[#0A3FB8] transition-colors"
        >
          Book Your Demo Now <ArrowRight className="w-4 h-4" />
        </a>
      </div>
    </div>
  );
}

/* ═══════════════════════─ MAIN PAGE ═══════════════════════*/
export default function LandingPage() {
  const [form, setForm] = useState({ first_name: "", last_name: "", email: "", phone: "", website: "" });
  const [heroForm, setHeroForm] = useState({ first_name: "", last_name: "", email: "", phone: "", website: "" });
  const [submitted, setSubmitted] = useState(false);
  const [heroSubmitted, setHeroSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [heroLoading, setHeroLoading] = useState(false);
  const [openFaq, setOpenFaq] = useState<number | null>(null);
  const [heroLoaded, setHeroLoaded] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [modalName, setModalName] = useState("");
  const [error, setError] = useState("");
  const [heroError, setHeroError] = useState("");

  const statsRef = useScrollAnimation(0.3);
  const statCounts = STATS.map((s) => useCountUp(s.value, 1500, statsRef.isVisible));

  useEffect(() => {
    const timer = setTimeout(() => setHeroLoaded(true), 100);
    return () => clearTimeout(timer);
  }, []);

  const handleHeroSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setHeroError("");
    if (!heroForm.email || !heroForm.first_name) {
      setHeroError("Please fill in your first name and email.");
      return;
    }
    setHeroLoading(true);
    try {
      const res = await fetch("/api/v1/leads/public", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          first_name: heroForm.first_name,
          last_name: heroForm.last_name,
          email: heroForm.email,
          phone: heroForm.phone,
          website: heroForm.website,
          business_name: `${heroForm.first_name} ${heroForm.last_name}`,
          notes: `Lead from landing page hero. Name: ${heroForm.first_name} ${heroForm.last_name}`,
          source: "landing_page_hero",
        }),
      });
      const data = await res.json();
      if (!res.ok) {
        setHeroError(data.detail || "Something went wrong. Please try again.");
      } else {
        setHeroSubmitted(true);
        setModalName(heroForm.first_name);
        setShowModal(true);
      }
    } catch (err) {
      setHeroError("Network error. Please check your connection and try again.");
    } finally {
      setHeroLoading(false);
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    if (!form.email || !form.first_name || !form.last_name) {
      setError("Please fill in all required fields (first name, last name, email).");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch("/api/v1/leads/public", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          first_name: form.first_name,
          last_name: form.last_name,
          email: form.email,
          phone: form.phone,
          website: form.website,
          business_name: `${form.first_name} ${form.last_name}`,
          notes: `Lead from landing page. Name: ${form.first_name} ${form.last_name}`,
          source: "landing_page",
        }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail || "Something went wrong. Please try again.");
      } else {
        setSubmitted(true);
        setModalName(form.first_name);
        setShowModal(true);
      }
    } catch (err) {
      setError("Network error. Please check your connection and try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (field: string) => (e: ChangeEvent<HTMLInputElement>) => {
    setForm((prev) => ({ ...prev, [field]: e.target.value }));
  };

  const handleHeroChange = (field: string) => (e: ChangeEvent<HTMLInputElement>) => {
    setHeroForm((prev) => ({ ...prev, [field]: e.target.value }));
  };

  return (
    <div className="min-h-screen bg-[#0F172A] text-[#F8FAFC] overflow-x-hidden">
      {/* Global Animations */}
      <style jsx global>{`
        @keyframes fadeInUp {
          from { opacity: 0; transform: translateY(40px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes pulse-glow {
          0%, 100% { box-shadow: 0 0 0 0 rgba(11, 79, 216, 0.4); }
          50% { box-shadow: 0 0 0 12px rgba(11, 79, 216, 0); }
        }
        .animate-fade-in-up {
          animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
          opacity: 0;
        }
        .animate-fade-in {
          animation: fadeIn 0.5s ease-out forwards;
          opacity: 0;
        }
        .animate-pulse-glow {
          animation: pulse-glow 2s ease-out infinite;
        }
        .delay-100 { animation-delay: 0.1s; }
        .delay-200 { animation-delay: 0.2s; }
        .delay-300 { animation-delay: 0.3s; }
        .delay-400 { animation-delay: 0.4s; }
        .delay-500 { animation-delay: 0.5s; }
        .delay-600 { animation-delay: 0.6s; }
        .delay-700 { animation-delay: 0.7s; }
      `}</style>

      {/* ═══════════════════ HERO ═══════════════════ */}
      <section className="relative min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8 overflow-hidden">
        <div className="absolute inset-0 bg-[#0F172A]">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center_bottom,rgba(11,79,216,0.12)_0%,transparent_70%)]" />
          <Image
            src="/landing/hero-bg.jpg"
            alt=""
            fill
            className="object-cover opacity-30"
            priority
          />
        </div>

        <div className="relative z-10 max-w-5xl mx-auto text-center pt-20 pb-16">
          {/* Pill badge */}
          <div className={`inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#0B4FD8]/10 border border-[#0B4FD8]/20 text-[#0B4FD8] text-sm font-medium mb-8 ${heroLoaded ? "animate-fade-in-up delay-200" : "opacity-0"}`}>
            <Sparkles className="w-4 h-4" />
            AI Automation for Any Business
          </div>

          {/* H1 */}
          <h1 className={`mb-6 ${heroLoaded ? "animate-fade-in-up delay-300" : "opacity-0"}`}>
            <span className="block text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold font-display tracking-tight leading-[1.05]">
              Your business works
            </span>
            <span className="block text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold font-display tracking-tight leading-[1.05] mt-1">
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#0B4FD8] to-[#22D3EE]">
                while you sleep.
              </span>
            </span>
          </h1>

          {/* Subheadline */}
          <p className={`text-lg sm:text-xl text-[#CBD5E1] max-w-2xl mx-auto mb-10 leading-relaxed ${heroLoaded ? "animate-fade-in-up delay-500" : "opacity-0"}`}>
            AI agents that answer calls, book appointments, follow up with leads,
            and handle customer service —{" "}
            <span className="text-[#F8FAFC] font-medium">24/7, across every channel.</span>
          </p>

          {/* Inline Lead Form */}
          <div className={`max-w-3xl mx-auto mb-6 ${heroLoaded ? "animate-fade-in-up delay-600" : "opacity-0"}`}>
            {!heroSubmitted ? (
              <form onSubmit={handleHeroSubmit}>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
                  <input
                    type="text"
                    required
                    placeholder="First Name"
                    value={heroForm.first_name}
                    onChange={handleHeroChange("first_name")}
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3.5 text-white placeholder-[#64748B] focus:outline-none focus:border-[#0B4FD8] focus:ring-1 focus:ring-[#0B4FD8]/30 text-sm transition-all"
                  />
                  <input
                    type="text"
                    placeholder="Last Name"
                    value={heroForm.last_name}
                    onChange={handleHeroChange("last_name")}
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3.5 text-white placeholder-[#64748B] focus:outline-none focus:border-[#0B4FD8] focus:ring-1 focus:ring-[#0B4FD8]/30 text-sm transition-all"
                  />
                  <input
                    type="email"
                    required
                    placeholder="Email"
                    value={heroForm.email}
                    onChange={handleHeroChange("email")}
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3.5 text-white placeholder-[#64748B] focus:outline-none focus:border-[#0B4FD8] focus:ring-1 focus:ring-[#0B4FD8]/30 text-sm transition-all"
                  />
                  <input
                    type="tel"
                    placeholder="Phone"
                    value={heroForm.phone}
                    onChange={handleHeroChange("phone")}
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3.5 text-white placeholder-[#64748B] focus:outline-none focus:border-[#0B4FD8] focus:ring-1 focus:ring-[#0B4FD8]/30 text-sm transition-all"
                  />
                  <button
                    type="submit"
                    disabled={heroLoading}
                    className="w-full py-3.5 rounded-xl bg-[#0B4FD8] text-white font-semibold hover:bg-[#0A3FB8] transition-all disabled:opacity-60 flex items-center justify-center gap-2 animate-pulse-glow"
                  >
                    {heroLoading ? (
                      <><Loader2 className="w-4 h-4 animate-spin" />Sending...</>
                    ) : (
                      <><Zap className="w-4 h-4" />Get Free Analysis</>
                    )}
                  </button>
                </div>
              </form>
            ) : (
              <div className="bg-[#10B981]/10 border border-[#10B981]/20 rounded-xl p-6 text-center">
                <CheckCircle className="w-12 h-12 text-[#10B981] mx-auto mb-3" />
                <h3 className="text-xl font-bold text-white mb-2">Thank you, {heroForm.first_name}!</h3>
                <p className="text-[#CBD5E1] mb-4">We&apos;ve received your info. Our team will send your personalized AI automation report within 24 hours.</p>
                <a href="https://cal.com/ender-ocando-lfxtkn/15min" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 text-[#0B4FD8] hover:text-[#22D3EE] font-medium transition-colors">
                  Book Your Demo Now <ArrowRight className="w-4 h-4" />
                </a>
              </div>
            )}
          </div>

          {heroError && (
            <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-3 text-center text-red-400 text-sm mb-4">
              {heroError}
            </div>
          )}
          {/* Trust microcopy */}
          <div className={`flex items-center justify-center gap-2 text-sm text-[#64748B] ${heroLoaded ? "animate-fade-in delay-700" : "opacity-0"}`}>
            <Lock className="w-3.5 h-3.5" />
            <span>No spam. We analyze your business and reply within 24 hours.</span>
          </div>
        </div>
      </section>

      {/* ═══════════════════ TRUST BAR ═══════════════════ */}
      <section className="py-10 px-4 sm:px-6 lg:px-8 bg-[#1E293B] border-t border-[#334155]">
        <AnimatedSection className="max-w-6xl mx-auto">
          <div className="flex flex-wrap items-center justify-center gap-6 md:gap-10 mb-4">
            {INDUSTRIES.map((ind) => (
              <div key={ind.label} className="flex items-center gap-2 text-[#64748B]">
                <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center">
                  <ind.icon className="w-4 h-4" />
                </div>
                <span className="text-sm">{ind.label}</span>
              </div>
            ))}
          </div>
          <p className="text-center text-[#64748B] text-sm">
            Trusted by <span className="text-[#F8FAFC] font-medium">500+ businesses</span> across 6 industries
          </p>
        </AnimatedSection>
      </section>

      {/* ═══════════════════ PROBLEM ═══════════════════ */}
      <section className="py-24 md:py-32 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 md:gap-16 items-center">
            <AnimatedSection>
              <span className="text-xs font-medium text-[#64748B] uppercase tracking-widest mb-4 block">The Problem</span>
              <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold font-display tracking-tight leading-tight mb-6">
                Every missed call is a{" "}
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#0B4FD8] to-[#22D3EE]">lost customer.</span>
              </h2>
              <p className="text-[#CBD5E1] text-lg leading-relaxed mb-8">
                You can&apos;t be available 24/7. But your customers expect instant responses.
                While you sleep, eat, or spend time with family — potential customers are going to your competitors.
              </p>
              <div className="space-y-4">
                {[
                  "65% of customers expect immediate responses",
                  "After 5 minutes, lead quality drops 80%",
                  "Hiring staff for 24/7 coverage costs $5,000+/month",
                ].map((item) => (
                  <div key={item} className="flex items-start gap-3">
                    <div className="w-5 h-5 rounded-full bg-[#0B4FD8]/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <CheckCircle className="w-3 h-3 text-[#0B4FD8]" />
                    </div>
                    <span className="text-[#CBD5E1]">{item}</span>
                  </div>
                ))}
              </div>
            </AnimatedSection>
            <AnimatedSection delay={0.2} className="relative">
              <div className="relative rounded-2xl overflow-hidden aspect-[4/3]">
                <Image
                  src="/landing/problem-owner.jpg"
                  alt="Business owner working late at night"
                  fill
                  className="object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-[#0F172A]/40 to-transparent" />
              </div>
            </AnimatedSection>
          </div>
        </div>
      </section>

      {/* ═══════════════════ SOLUTION ═══════════════════ */}
      <section className="py-24 md:py-32 px-4 sm:px-6 lg:px-8 relative">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(11,79,216,0.06)_0%,transparent_70%)]" />
        <div className="relative z-10 max-w-6xl mx-auto text-center">
          <AnimatedSection>
            <span className="text-xs font-medium text-[#64748B] uppercase tracking-widest mb-4 block">The Solution</span>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold font-display tracking-tight leading-tight mb-6 max-w-3xl mx-auto">
              One AI. Every channel.{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#0B4FD8] to-[#22D3EE]">Zero overhead.</span>
            </h2>
            <p className="text-[#CBD5E1] text-lg leading-relaxed max-w-2xl mx-auto mb-12">
              Eko AI is your 24/7 receptionist, sales assistant, and customer support agent —
              trained specifically for your business. It answers calls, responds to WhatsApp,
              handles emails, and books appointments. All automatically.
            </p>
          </AnimatedSection>

          <AnimatedSection delay={0.2} className="mb-12">
            <div className="relative max-w-3xl mx-auto aspect-video rounded-2xl overflow-hidden">
              <Image
                src="/landing/ai-hub.jpg"
                alt="Eko AI connecting all your business channels"
                fill
                className="object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-[#0F172A]/60 via-transparent to-[#0F172A]/30" />
            </div>
          </AnimatedSection>

          <AnimatedSection delay={0.3}>
            <div className="flex flex-wrap items-center justify-center gap-8 text-[#64748B]">
              {[
                { icon: Phone, label: "Phone Calls" },
                { icon: MessageSquare, label: "WhatsApp" },
                { icon: Mail, label: "Email" },
                { icon: Calendar, label: "Calendar" },
              ].map((ch) => (
                <div key={ch.label} className="flex items-center gap-2">
                  <div className="w-10 h-10 rounded-xl bg-[#0B4FD8]/10 flex items-center justify-center">
                    <ch.icon className="w-5 h-5 text-[#0B4FD8]" />
                  </div>
                  <span className="text-sm">{ch.label}</span>
                </div>
              ))}
            </div>
          </AnimatedSection>
        </div>
      </section>

      {/* ═══════════════════ HOW IT WORKS ═══════════════════ */}
      <section className="py-24 md:py-32 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <AnimatedSection className="text-center mb-16">
            <span className="text-xs font-medium text-[#64748B] uppercase tracking-widest mb-4 block">How It Works</span>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold font-display tracking-tight">
              From demo to live in <span className="text-[#0B4FD8]">48 hours</span>
            </h2>
          </AnimatedSection>

          <div className="grid md:grid-cols-3 gap-6">
            {HOW_STEPS.map((step, i) => (
              <AnimatedSection key={step.step} delay={i * 0.15}>
                <div className="group p-8 rounded-2xl bg-[#1E293B] border border-[#334155] hover:border-[#0B4FD8]/40 transition-all duration-300 h-full hover:-translate-y-1">
                  <span className="text-5xl font-bold text-[#0B4FD8] font-display mb-4 block">{step.step}</span>
                  <h3 className="text-xl font-semibold text-[#F8FAFC] mb-3">{step.title}</h3>
                  <p className="text-[#CBD5E1] leading-relaxed text-sm">{step.desc}</p>
                </div>
              </AnimatedSection>
            ))}
          </div>
        </div>
      </section>

      {/* ═══════════════════ FEATURES ═══════════════════ */}
      <section className="py-24 md:py-32 px-4 sm:px-6 lg:px-8 bg-[#1E293B]/30">
        <div className="max-w-6xl mx-auto">
          <AnimatedSection className="text-center mb-16">
            <span className="text-xs font-medium text-[#64748B] uppercase tracking-widest mb-4 block">Capabilities</span>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold font-display tracking-tight">
              One agent. <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#0B4FD8] to-[#22D3EE]">Unlimited tasks.</span>
            </h2>
          </AnimatedSection>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {FEATURES.map((feat, i) => (
              <AnimatedSection key={feat.title} delay={i * 0.1}>
                <div className="group p-6 rounded-xl border-b border-[#334155] hover:border-[#0B4FD8]/30 transition-all">
                  <div className="w-12 h-12 rounded-xl bg-[#0B4FD8]/10 flex items-center justify-center mb-4 group-hover:bg-[#0B4FD8]/20 transition-colors">
                    <feat.icon className="w-6 h-6 text-[#0B4FD8]" />
                  </div>
                  <h3 className="text-lg font-semibold text-[#F8FAFC] mb-2">{feat.title}</h3>
                  <p className="text-[#64748B] text-sm leading-relaxed">{feat.desc}</p>
                </div>
              </AnimatedSection>
            ))}
          </div>
        </div>
      </section>

      {/* ═══════════════════ STATS ═══════════════════ */}
      <section className="py-24 md:py-32 px-4 sm:px-6 lg:px-8 bg-[#1E293B]">
        <div className="max-w-6xl mx-auto">
          <div ref={statsRef.ref} className="grid grid-cols-2 lg:grid-cols-4 gap-8 mb-20">
            {STATS.map((stat, i) => (
              <div key={stat.label} className="text-center">
                <div className="text-4xl sm:text-5xl font-bold text-[#F8FAFC] font-display mb-2">
                  {stat.value >= 1000 ? `${(statCounts[i] / 1000).toFixed(stat.value % 1000 === 0 ? 0 : 1)}k` : statCounts[i]}{stat.suffix}
                </div>
                <div className="text-[#64748B] text-sm">{stat.label}</div>
              </div>
            ))}
          </div>

          {/* Testimonials */}
          <AnimatedSection>
            <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
              <div className="bg-[#0F172A] rounded-2xl p-8 border border-[#334155]">
                <div className="flex items-center gap-4 mb-6">
                  <div className="w-14 h-14 rounded-full overflow-hidden relative flex-shrink-0">
                    <Image
                      src="/landing/testimonial-maria.jpg"
                      alt="Maria G."
                      fill
                      className="object-cover"
                    />
                  </div>
                  <div>
                    <div className="font-semibold text-[#F8FAFC]">Maria G.</div>
                    <div className="text-[#64748B] text-sm">Spa Owner, Miami</div>
                  </div>
                </div>
                <p className="text-[#CBD5E1] leading-relaxed italic">
                  &ldquo;We used to miss at least 5-10 calls every day. Since implementing Eko AI, we haven&apos;t missed a single opportunity. Our appointment bookings increased 40% in the first month.&rdquo;
                </p>
                <div className="flex gap-1 mt-4">
                  {[1, 2, 3, 4, 5].map((s) => <Sparkles key={s} className="w-4 h-4 text-[#C9A84C]" />)}
                </div>
              </div>
              <div className="bg-[#0F172A] rounded-2xl p-8 border border-[#334155]">
                <div className="flex items-center gap-4 mb-6">
                  <div className="w-14 h-14 rounded-full overflow-hidden relative flex-shrink-0">
                    <Image
                      src="/landing/testimonial-carlos.jpg"
                      alt="Carlos R."
                      fill
                      className="object-cover"
                    />
                  </div>
                  <div>
                    <div className="font-semibold text-[#F8FAFC]">Carlos R.</div>
                    <div className="text-[#64748B] text-sm">Restaurant Owner, Madrid</div>
                  </div>
                </div>
                <p className="text-[#CBD5E1] leading-relaxed italic">
                  &ldquo;Eko AI handles all our reservation calls and WhatsApp inquiries. It&apos;s like having a full-time receptionist that never sleeps. Our customers love the instant responses.&rdquo;
                </p>
                <div className="flex gap-1 mt-4">
                  {[1, 2, 3, 4, 5].map((s) => <Sparkles key={s} className="w-4 h-4 text-[#C9A84C]" />)}
                </div>
              </div>
            </div>
          </AnimatedSection>
        </div>
      </section>

      {/* ═══════════════════ LEAD FORM (PRIMARY) ═══════════════════ */}
      <section className="py-24 md:py-32 px-4 sm:px-6 lg:px-8">
        <div className="max-w-xl mx-auto">
          <AnimatedSection className="text-center mb-10">
            <h2 className="text-3xl sm:text-4xl font-bold font-display tracking-tight mb-4">
              Ready to never miss a{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#0B4FD8] to-[#22D3EE]">customer again?</span>
            </h2>
            <p className="text-[#CBD5E1] leading-relaxed">
              Tell us about your business and we&apos;ll send you a personalized AI automation analysis — completely free.
            </p>
          </AnimatedSection>

          <AnimatedSection delay={0.2}>
            {!submitted ? (
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-medium text-[#64748B] uppercase tracking-wider mb-2">First Name *</label>
                    <input type="text" required placeholder="John" value={form.first_name} onChange={handleChange("first_name")}
                      className="w-full bg-[#1E293B] border border-[#334155] rounded-xl px-4 py-3.5 text-white placeholder-[#64748B] focus:outline-none focus:border-[#0B4FD8] focus:ring-1 focus:ring-[#0B4FD8]/30 transition-all" />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-[#64748B] uppercase tracking-wider mb-2">Last Name *</label>
                    <input type="text" required placeholder="Smith" value={form.last_name} onChange={handleChange("last_name")}
                      className="w-full bg-[#1E293B] border border-[#334155] rounded-xl px-4 py-3.5 text-white placeholder-[#64748B] focus:outline-none focus:border-[#0B4FD8] focus:ring-1 focus:ring-[#0B4FD8]/30 transition-all" />
                  </div>
                </div>
                <div>
                  <label className="block text-xs font-medium text-[#64748B] uppercase tracking-wider mb-2">Email *</label>
                  <input type="email" required placeholder="john@yourbusiness.com" value={form.email} onChange={handleChange("email")}
                    className="w-full bg-[#1E293B] border border-[#334155] rounded-xl px-4 py-3.5 text-white placeholder-[#64748B] focus:outline-none focus:border-[#0B4FD8] focus:ring-1 focus:ring-[#0B4FD8]/30 transition-all" />
                </div>
                <div>
                  <label className="block text-xs font-medium text-[#64748B] uppercase tracking-wider mb-2">Phone *</label>
                  <input type="tel" required placeholder="+1 (555) 000-0000" value={form.phone} onChange={handleChange("phone")}
                    className="w-full bg-[#1E293B] border border-[#334155] rounded-xl px-4 py-3.5 text-white placeholder-[#64748B] focus:outline-none focus:border-[#0B4FD8] focus:ring-1 focus:ring-[#0B4FD8]/30 transition-all" />
                </div>
                <div>
                  <label className="block text-xs font-medium text-[#64748B] uppercase tracking-wider mb-2">Business Website</label>
                  <input type="url" placeholder="www.yourbusiness.com (optional)" value={form.website} onChange={handleChange("website")}
                    className="w-full bg-[#1E293B] border border-[#334155] rounded-xl px-4 py-3.5 text-white placeholder-[#64748B] focus:outline-none focus:border-[#0B4FD8] focus:ring-1 focus:ring-[#0B4FD8]/30 transition-all" />
                </div>
                <button type="submit" disabled={loading}
                  className="w-full py-4 rounded-xl bg-[#0B4FD8] text-white font-semibold text-lg hover:bg-[#0A3FB8] transition-all disabled:opacity-60 flex items-center justify-center gap-2 animate-pulse-glow mt-6">
                  {loading ? (
                    <><Loader2 className="w-5 h-5 animate-spin" />Sending...</>
                  ) : (
                    <><Zap className="w-5 h-5" />Get My Free AI Analysis</>
                  )}
                </button>
                {error && (
                  <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-3 text-center text-red-400 text-sm mt-4">
                    {error}
                  </div>
                )}
                <div className="flex items-center justify-center gap-2 text-sm text-[#64748B] pt-2">
                  <Lock className="w-3.5 h-3.5" />
                  <span>Your information is secure. We never share your data.</span>
                </div>
                <div className="text-center pt-2">
                  <a href="https://cal.com/ender-ocando-lfxtkn/15min" target="_blank" rel="noopener noreferrer"
                    className="text-[#0B4FD8] hover:text-[#22D3EE] text-sm font-medium transition-colors inline-flex items-center gap-1">
                    Prefer to talk? Book a 15-min call <ArrowRight className="w-3.5 h-3.5" />
                  </a>
                </div>
              </form>
            ) : (
              <div className="bg-[#10B981]/10 border border-[#10B981]/20 rounded-2xl p-10 text-center">
                <CheckCircle className="w-16 h-16 text-[#10B981] mx-auto mb-4" />
                <h3 className="text-2xl font-bold text-white mb-3">Thank you, {form.first_name}!</h3>
                <p className="text-[#CBD5E1] mb-6 leading-relaxed">
                  We&apos;ve received your information. Our team will analyze your business and send your personalized AI automation report within 24 hours.
                </p>
                <a href="https://cal.com/ender-ocando-lfxtkn/15min" target="_blank" rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-[#0B4FD8] text-white font-semibold hover:bg-[#0A3FB8] transition-colors">
                  Book Your Demo Now <ArrowRight className="w-4 h-4" />
                </a>
              </div>
            )}
          </AnimatedSection>
        </div>
      </section>

      {/* ═══════════════════ FAQ ═══════════════════ */}
      <section className="py-24 md:py-32 px-4 sm:px-6 lg:px-8 bg-[#1E293B]/30">
        <div className="max-w-3xl mx-auto">
          <AnimatedSection className="text-center mb-12">
            <span className="text-xs font-medium text-[#64748B] uppercase tracking-widest mb-4 block">FAQ</span>
            <h2 className="text-3xl sm:text-4xl font-bold font-display tracking-tight">
              Questions? <span className="text-[#0B4FD8]">Answers.</span>
            </h2>
          </AnimatedSection>

          <AnimatedSection delay={0.2}>
            {FAQS.map((faq, i) => (
              <FAQItem key={i} item={faq} isOpen={openFaq === i} onToggle={() => setOpenFaq(openFaq === i ? null : i)} />
            ))}
          </AnimatedSection>
        </div>
      </section>

      {/* ═══════════════════ FINAL CTA ═══════════════════ */}
      <section className="py-32 md:py-40 px-4 sm:px-6 lg:px-8 relative">
        <div className="absolute inset-0 bg-gradient-to-b from-[#0F172A] to-[#0A1628]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <AnimatedSection>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold font-display tracking-tight mb-6">
              Stop losing customers{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#0B4FD8] to-[#22D3EE]">to missed calls.</span>
            </h2>
            <p className="text-[#CBD5E1] text-lg leading-relaxed mb-10 max-w-xl mx-auto">
              Join 500+ businesses already using Eko AI to automate their customer interactions.
            </p>
          </AnimatedSection>

          <AnimatedSection delay={0.2} className="flex flex-col items-center gap-4">
            <button
              onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
              className="inline-flex items-center gap-2 px-10 py-4 rounded-xl bg-[#0B4FD8] text-white font-semibold text-lg hover:bg-[#0A3FB8] transition-colors animate-pulse-glow"
            >
              <Zap className="w-5 h-5" />
              Get My Free AI Analysis
            </button>
            <a href="https://cal.com/ender-ocando-lfxtkn/15min" target="_blank" rel="noopener noreferrer"
              className="text-[#0B4FD8] hover:text-[#22D3EE] font-medium transition-colors inline-flex items-center gap-1">
              Or book a 15-minute demo call <ArrowRight className="w-4 h-4" />
            </a>
          </AnimatedSection>
        </div>
      </section>

      {/* ═══════════════════ FOOTER ═══════════════════ */}
      <footer className="py-10 px-4 sm:px-6 lg:px-8 border-t border-[#334155]">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#0B4FD8] to-[#0A3FB8] flex items-center justify-center">
              <Zap className="w-4 h-4 text-white" />
            </div>
            <span className="font-display font-bold text-[#F8FAFC]">Eko <span className="text-[#0B4FD8]">AI</span></span>
          </div>
          <p className="text-[#64748B] text-sm">&copy; {new Date().getFullYear()} Eko AI Automation. All rights reserved.</p>
          <a href="mailto:contact@biz.ekoaiautomation.com" className="text-sm text-[#64748B] hover:text-[#CBD5E1] transition-colors">
            contact@biz.ekoaiautomation.com
          </a>
        </div>
      </footer>

      {/* Success Modal */}
      <SuccessModal open={showModal} onClose={() => setShowModal(false)} name={modalName} />
    </div>
  );
}
