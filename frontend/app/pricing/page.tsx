"use client";

import { useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  Zap,
  Check,
  ArrowRight,
  Sparkles,
  Phone,
  Users,
  MessageSquare,
  Plus,
  Minus,
} from "lucide-react";
import {
  SiTwilio,
  SiStripe,
  SiResend,
  SiWhatsapp,
  SiGooglecalendar,
  SiBuffer,
  SiHubspot,
} from "react-icons/si";
import { useT } from "@/contexts/I18nProvider";
import LanguageSelector from "@/components/LanguageSelector";
import ROICalculator from "@/components/pricing/ROICalculator";
import AddonsSection from "@/components/pricing/AddonsSection";
import GrowthVerticalTabs from "@/components/pricing/GrowthVerticalTabs";

const CAL_URL = "https://cal.com/ender-ocando-lfxtkn/15min";

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" as const } },
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.12, delayChildren: 0.05 },
  },
};

// Pricing v2 (Council 2026-05-24): annual = 20% off the monthly equivalent
// (you pay ~10 months for 12). Matches Stripe "save 2 months" framing.
const ANNUAL_DISCOUNT = 0.20;
const toAnnualMonthly = (monthly: number) =>
  Math.round(monthly * (1 - ANNUAL_DISCOUNT));

// Pricing v2 (Council 2026-05-24). Starter horizontal, Growth has 3 verticals at the same
// price ($749), Enterprise combines all 3. Hardware runs client-side → high margin model.
// Existing customers stay on legacy pricing — only NEW signups see these tiers.
const PLANS = [
  {
    id: "starter",
    monthly: 249,
    popular: false,
    trial: true,
    features: 7,
    hasVerticals: false,
    href: CAL_URL,
  },
  {
    id: "growth",
    monthly: 749,
    popular: true,
    trial: false,
    features: 7, // common features only; verticals rendered by GrowthVerticalTabs
    hasVerticals: true,
    href: CAL_URL,
  },
  {
    id: "enterprise",
    monthly: 1999,
    popular: false,
    trial: false,
    features: 9,
    hasVerticals: false,
    href: CAL_URL,
  },
] as const;

const FAQ_KEYS = ["q1", "q2", "q3", "q4", "q5", "q6"] as const;

// Native integrations strip. VAPI uses lucide Phone as proxy (no SiVapi).
const INTEGRATIONS = [
  { Icon: Phone, label: "VAPI", color: "#00B86B" },
  { Icon: SiTwilio, label: "Twilio", color: "#F22F46" },
  { Icon: SiGooglecalendar, label: "Google Calendar", color: "#4285F4" },
  { Icon: SiResend, label: "Resend", color: "#FFFFFF" },
  { Icon: SiStripe, label: "Stripe", color: "#635BFF" },
  { Icon: SiBuffer, label: "Buffer", color: "#168EEA" },
  { Icon: SiWhatsapp, label: "WhatsApp", color: "#25D366" },
  { Icon: SiHubspot, label: "HubSpot", color: "#FF7A59" },
];

type FaqKey = (typeof FAQ_KEYS)[number];

function FAQItem({
  qKey,
  aKey,
  isOpen,
  onToggle,
}: {
  qKey: string;
  aKey: string;
  isOpen: boolean;
  onToggle: () => void;
}) {
  const { t } = useT();
  return (
    <div className="rounded-xl border border-white/10 bg-white/[0.02] overflow-hidden">
      <button
        type="button"
        onClick={onToggle}
        className="w-full flex items-center justify-between gap-3 px-5 py-4 text-left hover:bg-white/[0.03] transition-colors"
        aria-expanded={isOpen}
      >
        <span className="text-sm font-medium text-white">{t(qKey as never)}</span>
        {isOpen ? (
          <Minus className="w-4 h-4 text-eko-violet shrink-0" aria-hidden />
        ) : (
          <Plus className="w-4 h-4 text-gray-500 shrink-0" aria-hidden />
        )}
      </button>
      {isOpen && (
        <div className="px-5 pb-4 -mt-1 text-sm text-gray-400 leading-relaxed">
          {t(aKey as never)}
        </div>
      )}
    </div>
  );
}

export default function PricingPage() {
  const { t } = useT();
  const [billing, setBilling] = useState<"monthly" | "annual">("monthly");
  const [openFaq, setOpenFaq] = useState<FaqKey | null>("q1");

  return (
    <div className="min-h-screen bg-eko-noir">
      {/* Navbar */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-eko-noir/80 backdrop-blur-md border-b border-white/5">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-eko-violet to-eko-magenta flex items-center justify-center">
              <Zap className="w-5 h-5 text-white" />
            </div>
            <span className="font-display font-bold text-lg text-white">
              Eko <span className="text-eko-violet">AI</span>
            </span>
          </Link>
          <div className="hidden md:flex items-center gap-6">
            <Link href="/#como-funciona" className="text-sm text-gray-400 hover:text-white transition-colors">
              {t("home.nav.how_it_works")}
            </Link>
            <Link href="/#industrias" className="text-sm text-gray-400 hover:text-white transition-colors">
              {t("home.nav.industries")}
            </Link>
            <Link href="/pricing" className="text-sm text-eko-violet font-medium">
              {t("home.nav.pricing")}
            </Link>
            <LanguageSelector />
            <a
              href={CAL_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm px-4 py-2 rounded-lg bg-eko-violet text-white font-medium hover:bg-eko-violet-dark transition-colors"
            >
              {t("home.nav.book_demo")}
            </a>
          </div>
          <div className="md:hidden flex items-center gap-2">
            <LanguageSelector />
            <a
              href={CAL_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs px-3 py-1.5 rounded-lg bg-eko-violet text-white font-medium hover:bg-eko-violet-dark transition-colors"
            >
              {t("home.nav.book_demo")}
            </a>
          </div>
        </div>
      </nav>

      {/* Header */}
      <section className="relative pt-32 pb-12 px-4 sm:px-6 lg:px-8 text-center overflow-hidden">
        <div aria-hidden className="absolute inset-0 -z-10 pointer-events-none">
          <div className="absolute top-32 left-1/2 -translate-x-1/2 w-[40rem] h-[40rem] rounded-full bg-eko-violet/15 blur-[120px]" />
        </div>
        <motion.div
          initial="hidden"
          animate="visible"
          variants={staggerContainer}
          className="max-w-3xl mx-auto"
        >
          <motion.div
            variants={fadeUp}
            className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-eko-violet/10 border border-eko-violet/20 text-eko-violet text-xs font-medium mb-6"
          >
            <Sparkles className="w-3.5 h-3.5" />
            {t("pricing.hero.badge")}
          </motion.div>
          <motion.h1
            variants={fadeUp}
            className="text-4xl sm:text-5xl lg:text-6xl font-bold font-display text-white mb-4 leading-[1.1]"
          >
            {t("pricing.hero.title_part1")}{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-eko-violet via-eko-magenta to-eko-pink">
              {t("pricing.hero.title_highlight")}
            </span>
          </motion.h1>
          <motion.p variants={fadeUp} className="text-lg text-gray-400 max-w-xl mx-auto">
            {t("pricing.hero.subtitle")}
          </motion.p>
        </motion.div>
      </section>

      {/* Billing cycle toggle (Monthly / Annual save 20%) */}
      <section className="pb-10 px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-center">
          <div
            role="tablist"
            className="inline-flex items-center p-1 rounded-full border border-white/10 bg-white/[0.03]"
          >
            <button
              type="button"
              role="tab"
              aria-selected={billing === "monthly"}
              onClick={() => setBilling("monthly")}
              className={`px-5 py-2 rounded-full text-sm font-medium transition-all ${
                billing === "monthly"
                  ? "bg-eko-violet text-white shadow-md shadow-eko-violet/30"
                  : "text-gray-400 hover:text-white"
              }`}
            >
              {t("pricing.billing.monthly")}
            </button>
            <button
              type="button"
              role="tab"
              aria-selected={billing === "annual"}
              onClick={() => setBilling("annual")}
              className={`px-5 py-2 rounded-full text-sm font-medium transition-all flex items-center gap-2 ${
                billing === "annual"
                  ? "bg-eko-violet text-white shadow-md shadow-eko-violet/30"
                  : "text-gray-400 hover:text-white"
              }`}
            >
              {t("pricing.billing.annual")}
              <span
                className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                  billing === "annual"
                    ? "bg-eko-pink/30 text-white"
                    : "bg-eko-green/15 text-eko-green"
                }`}
              >
                {t("pricing.billing.save")}
              </span>
            </button>
          </div>
        </div>
      </section>

      {/* Pricing Cards */}
      <section className="pb-20 px-4 sm:px-6 lg:px-8">
        <motion.div
          variants={staggerContainer}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-50px" }}
          className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6"
        >
          {PLANS.map((plan) => {
            const featureKeys = Array.from(
              { length: plan.features },
              (_, i) => `pricing.${plan.id}.f${i + 1}`,
            );
            const displayPrice =
              billing === "annual" ? toAnnualMonthly(plan.monthly) : plan.monthly;
            return (
              <motion.div
                key={plan.id}
                variants={fadeUp}
                className={`relative rounded-2xl border p-8 flex flex-col ${
                  plan.popular
                    ? "border-eko-violet/40 bg-gradient-to-b from-eko-violet/15 via-eko-magenta/5 to-transparent shadow-xl shadow-eko-violet/10"
                    : "border-white/5 bg-white/[0.02]"
                }`}
              >
                {plan.popular && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full bg-gradient-to-r from-eko-violet to-eko-magenta text-white text-xs font-medium whitespace-nowrap">
                    {t("pricing.popular")}
                  </div>
                )}

                {plan.trial && (
                  <div className="absolute -top-3 right-4 px-2.5 py-1 rounded-full bg-eko-green/15 border border-eko-green/30 text-eko-green text-xs font-medium whitespace-nowrap">
                    {t("pricing.trial_badge")}
                  </div>
                )}

                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-white mb-2">
                    {t(`pricing.${plan.id}.name` as never)}
                  </h3>
                  <div className="flex items-baseline gap-1 mb-1">
                    <span className="text-4xl font-bold text-white">${displayPrice}</span>
                    <span className="text-gray-500">{t("pricing.per_month")}</span>
                  </div>
                  <p className="text-xs text-gray-600 mb-3 h-4">
                    {billing === "annual" ? t("pricing.billing.billed_annually") : ""}
                  </p>
                  <p className="text-gray-500 text-sm">
                    {t(`pricing.${plan.id}.tagline` as never)}
                  </p>
                </div>

                {/* Stats highlight box — voice min + contacts + AI replies */}
                <div className="grid grid-cols-3 gap-2 mb-6 p-3 rounded-xl bg-white/[0.03] border border-white/5">
                  <div className="text-center">
                    <Phone className="w-3.5 h-3.5 text-eko-violet mx-auto mb-1" />
                    <div className="text-white font-semibold text-sm">
                      {t(`pricing.${plan.id}.voice_min_value` as never)}
                    </div>
                    <div className="text-[10px] text-gray-500 leading-tight">
                      {t("pricing.stats.voice_min")}
                    </div>
                  </div>
                  <div className="text-center border-x border-white/5">
                    <Users className="w-3.5 h-3.5 text-eko-magenta mx-auto mb-1" />
                    <div className="text-white font-semibold text-sm">
                      {t(`pricing.${plan.id}.contacts_value` as never)}
                    </div>
                    <div className="text-[10px] text-gray-500 leading-tight">
                      {t("pricing.stats.contacts")}
                    </div>
                  </div>
                  <div className="text-center">
                    <MessageSquare className="w-3.5 h-3.5 text-eko-pink mx-auto mb-1" />
                    <div className="text-white font-semibold text-sm">
                      {t(`pricing.${plan.id}.ai_replies_value` as never)}
                    </div>
                    <div className="text-[10px] text-gray-500 leading-tight">
                      {t("pricing.stats.ai_replies")}
                    </div>
                  </div>
                </div>

                <ul className="space-y-3 mb-4 flex-1">
                  {(plan.hasVerticals
                    ? Array.from({ length: 7 }, (_, i) => `pricing.growth.common.f${i + 1}`)
                    : featureKeys
                  ).map((key) => (
                    <li key={key} className="flex items-start gap-3">
                      <Check className="w-4 h-4 text-eko-green shrink-0 mt-0.5" />
                      <span className="text-gray-300 text-sm">{t(key as never)}</span>
                    </li>
                  ))}
                </ul>

                {plan.hasVerticals && <GrowthVerticalTabs />}

                <a
                  href={plan.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={`w-full py-3 rounded-xl font-semibold text-center flex items-center justify-center gap-2 transition-all ${
                    plan.popular
                      ? "bg-eko-violet text-white hover:bg-eko-violet-dark"
                      : "bg-white/5 border border-white/10 text-white hover:bg-white/10"
                  }`}
                >
                  {t(`pricing.${plan.id}.cta` as never)}
                  <ArrowRight className="w-4 h-4" />
                </a>
              </motion.div>
            );
          })}
        </motion.div>
      </section>

      {/* ROI Calculator (pricing v2) */}
      <section className="pb-16 px-4 sm:px-6 lg:px-8">
        <ROICalculator />
      </section>

      {/* Add-ons (pricing v2) */}
      <AddonsSection />

      {/* Integrations strip */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 border-t border-white/5">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6 }}
          className="max-w-5xl mx-auto text-center"
        >
          <h2 className="text-xl sm:text-2xl font-semibold text-white mb-2">
            {t("pricing.integrations.title")}
          </h2>
          <p className="text-gray-500 text-sm mb-8">
            {t("pricing.integrations.subtitle")}
          </p>
          <div className="flex flex-wrap items-center justify-center gap-x-10 gap-y-6">
            {INTEGRATIONS.map(({ Icon, label, color }) => (
              <div
                key={label}
                className="group flex items-center gap-2.5 text-gray-500 hover:text-white transition-colors cursor-default"
              >
                <Icon
                  className="w-6 h-6 transition-colors group-hover:opacity-100"
                  style={{ color }}
                  aria-hidden
                />
                <span className="font-medium text-sm">{label}</span>
              </div>
            ))}
          </div>
        </motion.div>
      </section>

      {/* FAQ inline (pricing v2) — 6 real questions + CTA at the end */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-white/[0.02] border-y border-white/5">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6 }}
          className="max-w-3xl mx-auto"
        >
          <div className="text-center mb-8">
            <h2 className="text-2xl sm:text-3xl font-bold text-white mb-2">{t("pricing.faq.title")}</h2>
            <p className="text-gray-400">{t("pricing.faq.subtitle")}</p>
          </div>

          <div className="space-y-2 mb-8">
            {FAQ_KEYS.map((qk) => (
              <FAQItem
                key={qk}
                qKey={`pricing.faq.${qk}.q`}
                aKey={`pricing.faq.${qk}.a`}
                isOpen={openFaq === qk}
                onToggle={() => setOpenFaq(openFaq === qk ? null : qk)}
              />
            ))}
          </div>

          <div className="text-center">
            <a
              href={CAL_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-8 py-3 rounded-xl bg-eko-violet text-white font-semibold hover:bg-eko-violet-dark transition-colors"
            >
              <Zap className="w-4 h-4" />
              {t("pricing.faq.cta")}
            </a>
          </div>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="py-10 px-4 sm:px-6 lg:px-8 border-t border-white/5">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-eko-violet to-eko-magenta flex items-center justify-center">
              <Zap className="w-4 h-4 text-white" />
            </div>
            <span className="font-display font-bold text-white">
              Eko <span className="text-eko-violet">AI</span>
            </span>
          </div>
          <p className="text-gray-600 text-sm">
            © {new Date().getFullYear()} Eko AI Automation. {t("home.footer.rights")}
          </p>
          <div className="flex items-center gap-4 text-sm text-gray-500">
            <a
              href="mailto:contact@biz.ekoaiautomation.com"
              className="hover:text-gray-300 transition-colors"
            >
              contact@biz.ekoaiautomation.com
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
