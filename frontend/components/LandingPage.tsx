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

const CAL_URL = "https://cal.com/ender-ocando-lfxtkn/15min";

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
    business_name: "",
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
    if (!form.email && !form.phone) return;
    setLoading(true);
    try {
      await fetch("/api/v1/leads/public", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          notes: `Lead captured from landing page. Industry: ${form.category || "N/A"}`,
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
    <div className="min-h-screen bg-eko-graphite">
      {/* Navbar */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-eko-graphite/80 backdrop-blur-md border-b border-white/5">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-eko-blue to-eko-blue-dark flex items-center justify-center">
              <Zap className="w-5 h-5 text-white" />
            </div>
            <span className="font-display font-bold text-lg text-white">
              Eko <span className="text-eko-blue">AI</span>
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
              className="text-sm px-4 py-2 rounded-lg bg-eko-blue text-white font-medium hover:bg-eko-blue-dark transition-colors"
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
              className="text-xs px-3 py-1.5 rounded-lg bg-eko-blue text-white font-medium hover:bg-eko-blue-dark transition-colors"
            >
              {t("home.nav.book_demo")}
            </a>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <motion.div
          initial="hidden"
          animate="visible"
          variants={staggerContainer}
          className="max-w-5xl mx-auto text-center"
        >
          <motion.div
            variants={fadeUp}
            className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-eko-blue/10 border border-eko-blue/20 text-eko-blue text-xs font-medium mb-6"
          >
            <Sparkles className="w-3.5 h-3.5" />
            {t("home.hero.badge")}
          </motion.div>
          <motion.h1
            variants={fadeUp}
            className="text-4xl sm:text-5xl lg:text-6xl font-bold font-display text-white leading-tight mb-6"
          >
            {t("home.hero.title_part1")}{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-eko-blue to-cyan-400">
              {t("home.hero.title_highlight")}
            </span>
          </motion.h1>
          <motion.p
            variants={fadeUp}
            className="text-lg sm:text-xl text-gray-400 max-w-2xl mx-auto mb-10 leading-relaxed"
          >
            {t("home.hero.subtitle_part1")}{" "}
            <span className="text-white font-medium">{t("home.hero.subtitle_emphasis")}</span>
            {t("home.hero.subtitle_part2")}
          </motion.p>
          <motion.div variants={fadeUp} className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
            <Link
              href={CAL_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-eko-blue text-white font-semibold hover:bg-eko-blue-dark transition-all flex items-center justify-center gap-2"
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

          <motion.div variants={fadeUp} className="flex flex-wrap items-center justify-center gap-8 text-gray-500 text-sm">
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
      </section>

      {/* Lead Capture Form */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-white/[0.02] border-y border-white/5">
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
                className="text-eko-blue hover:underline text-sm"
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
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <input
                    type="text"
                    required
                    placeholder={t("home.form.business_name")}
                    value={form.business_name}
                    onChange={(e) => setForm({ ...form, business_name: e.target.value })}
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-eko-blue text-sm"
                  />
                  <select
                    value={form.category}
                    onChange={(e) => setForm({ ...form, category: e.target.value })}
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-eko-blue text-sm appearance-none"
                  >
                    <option value="" className="bg-eko-graphite text-gray-500">{t("home.form.category_default")}</option>
                    <option value="spa" className="bg-eko-graphite">{t("home.form.category_spa")}</option>
                    <option value="restaurant" className="bg-eko-graphite">{t("home.form.category_restaurant")}</option>
                    <option value="clinic" className="bg-eko-graphite">{t("home.form.category_clinic")}</option>
                    <option value="gym" className="bg-eko-graphite">{t("home.form.category_gym")}</option>
                    <option value="retail" className="bg-eko-graphite">{t("home.form.category_retail")}</option>
                    <option value="pro" className="bg-eko-graphite">{t("home.form.category_pro")}</option>
                    <option value="other" className="bg-eko-graphite">{t("home.form.category_other")}</option>
                  </select>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <input
                    type="email"
                    placeholder={t("home.form.email")}
                    value={form.email}
                    onChange={(e) => setForm({ ...form, email: e.target.value })}
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-eko-blue text-sm"
                  />
                  <input
                    type="tel"
                    placeholder={t("home.form.phone")}
                    value={form.phone}
                    onChange={(e) => setForm({ ...form, phone: e.target.value })}
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-eko-blue text-sm"
                  />
                </div>
                <button
                  type="submit"
                  disabled={loading || (!form.email && !form.phone)}
                  className="w-full py-3 rounded-lg bg-eko-blue text-white font-semibold hover:bg-eko-blue-dark transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
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
                <div className="w-10 h-10 rounded-lg bg-eko-blue/10 flex items-center justify-center mb-4 group-hover:bg-eko-blue/20 transition-colors">
                  <ind.icon className="w-5 h-5 text-eko-blue" />
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
                  <feat.icon className="w-5 h-5 text-eko-blue" />
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
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-eko-blue to-eko-blue-dark flex items-center justify-center mx-auto mb-5">
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
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-eko-blue/5 to-transparent">
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
              className="w-full sm:w-auto px-8 py-4 rounded-xl bg-eko-blue text-white font-semibold hover:bg-eko-blue-dark transition-all flex items-center justify-center gap-2 text-lg"
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
            <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-eko-blue to-eko-blue-dark flex items-center justify-center">
              <Zap className="w-4 h-4 text-white" />
            </div>
            <span className="font-display font-bold text-white">
              Eko <span className="text-eko-blue">AI</span>
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
