"use client";

import { useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  Zap,
  Bot,
  Clock,
  TrendingUp,
  Shield,
  MessageSquare,
  Calendar,
  ArrowRight,
  CheckCircle,
  Loader2,
  Sparkles,
  UtensilsCrossed,
  Stethoscope,
  Dumbbell,
  Store,
  Briefcase,
} from "lucide-react";
import { useT } from "@/contexts/I18nProvider";
import LanguageSelector from "@/components/LanguageSelector";
import { SplineScene } from "@/components/ui/splite";

const CAL_URL = "https://cal.com/ender-ocando-lfxtkn/15min";

// Robot 3D scene (community remix in user workspace). Swap via spline.design
// editor → Export → Code → Next.js → Public URI.
const SPLINE_SCENE_URL =
  "https://prod.spline.design/wfmv3zVpU19sOZGs/scene.splinecode";

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" as const } },
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.08, delayChildren: 0.05 },
  },
};

export default function LandingPage() {
  const { t } = useT();

  const [form, setForm] = useState({
    website: "",
    email: "",
    phone: "",
    category: "",
  });
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const INDUSTRIES = [
    { icon: Sparkles, label: t("home.industries.spa.label"), desc: t("home.industries.spa.desc") },
    { icon: UtensilsCrossed, label: t("home.industries.restaurant.label"), desc: t("home.industries.restaurant.desc") },
    { icon: Stethoscope, label: t("home.industries.clinic.label"), desc: t("home.industries.clinic.desc") },
    { icon: Dumbbell, label: t("home.industries.gym.label"), desc: t("home.industries.gym.desc") },
    { icon: Store, label: t("home.industries.retail.label"), desc: t("home.industries.retail.desc") },
    { icon: Briefcase, label: t("home.industries.pro.label"), desc: t("home.industries.pro.desc") },
  ];

  const FEATURES = [
    { icon: Bot, title: t("home.features.f1.title"), desc: t("home.features.f1.desc") },
    { icon: Calendar, title: t("home.features.f2.title"), desc: t("home.features.f2.desc") },
    { icon: MessageSquare, title: t("home.features.f3.title"), desc: t("home.features.f3.desc") },
    { icon: TrendingUp, title: t("home.features.f4.title"), desc: t("home.features.f4.desc") },
    { icon: Clock, title: t("home.features.f5.title"), desc: t("home.features.f5.desc") },
    { icon: Shield, title: t("home.features.f6.title"), desc: t("home.features.f6.desc") },
  ];

  const HOW_IT_WORKS = [
    { step: "01", title: t("home.how.s1.title"), desc: t("home.how.s1.desc") },
    { step: "02", title: t("home.how.s2.title"), desc: t("home.how.s2.desc") },
    { step: "03", title: t("home.how.s3.title"), desc: t("home.how.s3.desc") },
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Website is required (seeds the AI analysis). Plus need at least one contact channel.
    if (!form.website) return;
    if (!form.email && !form.phone) return;
    setLoading(true);
    try {
      await fetch("/api/v1/leads/public", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          notes: `Lead captured from landing page. Website: ${form.website}. Industry: ${form.category || "N/A"}`,
        }),
      });
      setSubmitted(true);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

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
            <a href="#como-funciona" className="text-sm text-gray-400 hover:text-white transition-colors">
              {t("home.nav.how_it_works")}
            </a>
            <a href="#industrias" className="text-sm text-gray-400 hover:text-white transition-colors">
              {t("home.nav.industries")}
            </a>
            <Link href="/pricing" className="text-sm text-gray-400 hover:text-white transition-colors">
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
          {/* Mobile: just selector + CTA */}
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

      {/* Hero */}
      <section className="relative pt-32 pb-20 px-4 sm:px-6 lg:px-8 overflow-hidden">
        {/* Ambient glow behind hero */}
        <div aria-hidden className="absolute inset-0 -z-10 pointer-events-none">
          <div className="absolute top-1/2 left-1/4 -translate-x-1/2 -translate-y-1/2 w-[36rem] h-[36rem] rounded-full bg-eko-violet/20 blur-[120px]" />
          <div className="absolute top-1/3 right-1/4 translate-x-1/2 w-[26rem] h-[26rem] rounded-full bg-eko-magenta/15 blur-[100px]" />
        </div>

        <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-10 lg:gap-12 items-center">
          {/* Left: copy + CTAs */}
          <motion.div
            initial="hidden"
            animate="visible"
            variants={staggerContainer}
            className="text-center lg:text-left"
          >
            <motion.div
              variants={fadeUp}
              className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-eko-violet/10 border border-eko-violet/20 text-eko-violet text-xs font-medium mb-6"
            >
              <Sparkles className="w-3.5 h-3.5" />
              {t("home.hero.badge")}
            </motion.div>
            <motion.h1
              variants={fadeUp}
              className="text-4xl sm:text-5xl lg:text-6xl font-bold font-display text-white leading-tight mb-6"
            >
              {t("home.hero.title_part1")}{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-eko-violet via-eko-magenta to-eko-pink">
                {t("home.hero.title_highlight")}
              </span>
            </motion.h1>
            <motion.p
              variants={fadeUp}
              className="text-lg sm:text-xl text-gray-400 max-w-2xl mx-auto lg:mx-0 mb-10 leading-relaxed"
            >
              {t("home.hero.subtitle_part1")}{" "}
              <span className="text-white font-medium">{t("home.hero.subtitle_emphasis")}</span>
              {t("home.hero.subtitle_part2")}
            </motion.p>
            <motion.div
              variants={fadeUp}
              className="flex flex-col sm:flex-row items-center lg:justify-start justify-center gap-4 mb-10"
            >
              <Link
                href={CAL_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-eko-violet text-white font-semibold hover:bg-eko-violet-dark transition-all flex items-center justify-center gap-2"
              >
                <Calendar className="w-5 h-5" />
                {t("home.hero.cta_primary")}
              </Link>
              <Link
                href="/pricing"
                className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-white/5 border border-white/10 text-white font-semibold hover:bg-white/10 transition-all flex items-center justify-center gap-2"
              >
                {t("home.hero.cta_secondary")}
                <ArrowRight className="w-4 h-4" />
              </Link>
            </motion.div>

            <motion.div
              variants={fadeUp}
              className="flex flex-wrap items-center lg:justify-start justify-center gap-x-6 gap-y-2 text-gray-500 text-sm"
            >
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-eko-green" />
                <span>{t("home.hero.proof_setup")}</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-eko-green" />
                <span>{t("home.hero.proof_no_contract")}</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-eko-green" />
                <span>{t("home.hero.proof_cancel")}</span>
              </div>
            </motion.div>
          </motion.div>

          {/* Right: 3D robot scene (desktop only — heavy asset, mobile users skip).
              Radial mask fades canvas edges so the rectangular Spline bg blends
              into the page (no visible "box"). Ambient glow behind extends the
              violet/magenta spillover beyond the container. Clicking anywhere
              (including the baked-in "Get in touch" button) scrolls to the form. */}
          <div className="hidden lg:block relative w-full h-[480px] xl:h-[560px]">
            <div
              aria-hidden
              className="absolute inset-[-12%] -z-10 pointer-events-none"
              style={{
                background:
                  "radial-gradient(ellipse 65% 70% at 50% 55%, rgba(124,58,237,0.22) 0%, rgba(217,70,239,0.10) 38%, transparent 72%)",
              }}
            />
            <motion.div
              initial={{ opacity: 0, scale: 0.92 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 1, delay: 0.25, ease: "easeOut" }}
              onClick={() => {
                document
                  .getElementById("lead-form")
                  ?.scrollIntoView({ behavior: "smooth" });
              }}
              role="button"
              tabIndex={0}
              aria-label="Scroll to lead form"
              className="w-full h-full cursor-pointer"
              style={{
                maskImage:
                  "radial-gradient(ellipse 75% 80% at 50% 50%, black 60%, transparent 95%)",
                WebkitMaskImage:
                  "radial-gradient(ellipse 75% 80% at 50% 50%, black 60%, transparent 95%)",
              }}
            >
              <SplineScene scene={SPLINE_SCENE_URL} className="w-full h-full" />
            </motion.div>
          </div>
        </div>
      </section>

      {/* Lead Capture Form */}
      <section
        id="lead-form"
        className="py-16 px-4 sm:px-6 lg:px-8 bg-white/[0.02] border-y border-white/5"
      >
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6 }}
          className="max-w-xl mx-auto"
        >
          {submitted ? (
            <div className="text-center py-8">
              <CheckCircle className="w-14 h-14 text-eko-green mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-white mb-2">{t("home.form.success_title")}</h2>
              <p className="text-gray-400 mb-4">{t("home.form.success_message")}</p>
              <a
                href={CAL_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="text-eko-violet hover:underline text-sm"
              >
                {t("home.form.success_link")}
              </a>
            </div>
          ) : (
            <>
              <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-white mb-2">{t("home.form.title")}</h2>
                <p className="text-gray-400 text-sm">{t("home.form.subtitle")}</p>
              </div>
              <form onSubmit={handleSubmit} className="space-y-4">
                {/* Row 1: website (full width) — the AI analysis seed */}
                <div>
                  <input
                    type="url"
                    required
                    placeholder={t("home.form.website")}
                    value={form.website}
                    onChange={(e) => setForm({ ...form, website: e.target.value })}
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-eko-violet text-sm"
                  />
                  <p className="text-xs text-eko-violet/80 pl-1 mt-1.5">
                    {t("home.form.website_help")}
                  </p>
                </div>

                {/* Row 2: category + email */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <select
                    value={form.category}
                    onChange={(e) => setForm({ ...form, category: e.target.value })}
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-eko-violet text-sm appearance-none"
                  >
                    <option value="" className="bg-eko-noir text-gray-500">{t("home.form.category_default")}</option>
                    <option value="spa" className="bg-eko-noir">{t("home.form.category_spa")}</option>
                    <option value="restaurant" className="bg-eko-noir">{t("home.form.category_restaurant")}</option>
                    <option value="clinic" className="bg-eko-noir">{t("home.form.category_clinic")}</option>
                    <option value="gym" className="bg-eko-noir">{t("home.form.category_gym")}</option>
                    <option value="retail" className="bg-eko-noir">{t("home.form.category_retail")}</option>
                    <option value="pro" className="bg-eko-noir">{t("home.form.category_pro")}</option>
                    <option value="other" className="bg-eko-noir">{t("home.form.category_other")}</option>
                  </select>
                  <input
                    type="email"
                    placeholder={t("home.form.email")}
                    value={form.email}
                    onChange={(e) => setForm({ ...form, email: e.target.value })}
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-eko-violet text-sm"
                  />
                </div>

                {/* Row 3: phone full width (optional secondary contact) */}
                <div>
                  <input
                    type="tel"
                    placeholder={t("home.form.phone")}
                    value={form.phone}
                    onChange={(e) => setForm({ ...form, phone: e.target.value })}
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-eko-violet text-sm"
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading || !form.website || (!form.email && !form.phone)}
                  className="w-full py-3 rounded-lg bg-eko-violet text-white font-semibold hover:bg-eko-violet-dark transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      {t("home.form.submitting")}
                    </>
                  ) : (
                    <>
                      <Zap className="w-4 h-4" />
                      {t("home.form.submit")}
                    </>
                  )}
                </button>
                <p className="text-center text-gray-600 text-xs">{t("home.form.disclaimer")}</p>
              </form>
            </>
          )}
        </motion.div>
      </section>

      {/* Industries */}
      <section id="industrias" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.6 }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl font-bold text-white mb-3">{t("home.industries.title")}</h2>
            <p className="text-gray-400 max-w-xl mx-auto">{t("home.industries.subtitle")}</p>
          </motion.div>
          <motion.div
            variants={staggerContainer}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-50px" }}
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"
          >
            {INDUSTRIES.map((ind) => (
              <motion.div
                key={ind.label}
                variants={fadeUp}
                className="group p-6 rounded-xl border border-white/5 bg-white/[0.02] hover:bg-white/5 hover:border-white/10 transition-all"
              >
                <div className="w-10 h-10 rounded-lg bg-eko-violet/10 flex items-center justify-center mb-4 group-hover:bg-eko-violet/20 transition-colors">
                  <ind.icon className="w-5 h-5 text-eko-violet" />
                </div>
                <h3 className="text-white font-semibold mb-1">{ind.label}</h3>
                <p className="text-gray-500 text-sm">{ind.desc}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white/[0.02] border-y border-white/5">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.6 }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl font-bold text-white mb-3">{t("home.features.title")}</h2>
            <p className="text-gray-400 max-w-xl mx-auto">{t("home.features.subtitle")}</p>
          </motion.div>
          <motion.div
            variants={staggerContainer}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-50px" }}
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"
          >
            {FEATURES.map((feat) => (
              <motion.div key={feat.title} variants={fadeUp} className="p-6 rounded-xl">
                <div className="w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center mb-4">
                  <feat.icon className="w-5 h-5 text-eko-violet" />
                </div>
                <h3 className="text-white font-semibold mb-2">{feat.title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{feat.desc}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* How it Works */}
      <section id="como-funciona" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.6 }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl font-bold text-white mb-3">{t("home.how.title")}</h2>
            <p className="text-gray-400 max-w-xl mx-auto">{t("home.how.subtitle")}</p>
          </motion.div>
          <motion.div
            variants={staggerContainer}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-50px" }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8"
          >
            {HOW_IT_WORKS.map((step) => (
              <motion.div key={step.step} variants={fadeUp} className="text-center">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-eko-violet to-eko-magenta flex items-center justify-center mx-auto mb-5">
                  <span className="text-white font-bold text-lg">{step.step}</span>
                </div>
                <h3 className="text-white font-semibold text-lg mb-2">{step.title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{step.desc}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-eko-violet/10 via-eko-magenta/5 to-transparent">
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6 }}
          className="max-w-3xl mx-auto text-center"
        >
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">{t("home.cta.title")}</h2>
          <p className="text-gray-400 text-lg mb-8">{t("home.cta.subtitle")}</p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href={CAL_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-8 py-4 rounded-xl bg-eko-violet text-white font-semibold hover:bg-eko-violet-dark transition-all flex items-center justify-center gap-2 text-lg"
            >
              <Calendar className="w-5 h-5" />
              {t("home.cta.primary")}
            </Link>
            <Link
              href="/pricing"
              className="w-full sm:w-auto px-8 py-4 rounded-xl bg-white/5 border border-white/10 text-white font-semibold hover:bg-white/10 transition-all"
            >
              {t("home.cta.secondary")}
            </Link>
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
