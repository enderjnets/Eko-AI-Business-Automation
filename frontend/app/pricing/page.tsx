"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import {
  Zap,
  Check,
  ArrowRight,
  Sparkles,
  Building2,
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
    transition: { staggerChildren: 0.12, delayChildren: 0.05 },
  },
};

// Plans authored against the real platform capabilities (Dashboard MODULES +
// backend services audit). All features below correspond to working code in
// the app — no vaporware. Content Studio (social media management for 3
// networks) is intentionally Enterprise-only per user constraint.
const PLANS = [
  {
    id: "starter",
    price: 99,
    popular: false,
    features: 7,
    href: CAL_URL,
  },
  {
    id: "growth",
    price: 199,
    popular: true,
    features: 9,
    href: CAL_URL,
  },
  {
    id: "enterprise",
    price: 299,
    popular: false,
    features: 9,
    href: CAL_URL,
  },
] as const;

export default function PricingPage() {
  const { t } = useT();

  return (
    <div className="min-h-screen bg-eko-noir">
      {/* Navbar (mirrors home structure for consistency) */}
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

      {/* Header — hero */}
      <section className="relative pt-32 pb-12 px-4 sm:px-6 lg:px-8 text-center overflow-hidden">
        {/* Ambient violet glow */}
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

      {/* Setup Fee Banner */}
      <section className="pb-12 px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6 }}
          className="max-w-2xl mx-auto"
        >
          <div className="flex items-start gap-4 p-5 rounded-xl bg-gold/5 border border-gold/20">
            <Building2 className="w-8 h-8 text-gold shrink-0 mt-0.5" />
            <div>
              <p className="text-white font-medium mb-1">
                {t("pricing.setup.label")}{" "}
                <span className="text-gold">{t("pricing.setup.price")}</span>
              </p>
              <p className="text-gray-500 text-sm leading-relaxed">
                {t("pricing.setup.desc")}
              </p>
            </div>
          </div>
        </motion.div>
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
              (_, i) => `pricing.${plan.id}.f${i + 1}` as const,
            );
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
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-white mb-2">
                    {t(`pricing.${plan.id}.name` as never)}
                  </h3>
                  <div className="flex items-baseline gap-1 mb-3">
                    <span className="text-4xl font-bold text-white">${plan.price}</span>
                    <span className="text-gray-500">{t("pricing.per_month")}</span>
                  </div>
                  <p className="text-gray-500 text-sm">
                    {t(`pricing.${plan.id}.tagline` as never)}
                  </p>
                </div>

                <ul className="space-y-3 mb-8 flex-1">
                  {featureKeys.map((key) => (
                    <li key={key} className="flex items-start gap-3">
                      <Check className="w-4 h-4 text-eko-green shrink-0 mt-0.5" />
                      <span className="text-gray-300 text-sm">{t(key as never)}</span>
                    </li>
                  ))}
                </ul>

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

      {/* FAQ Teaser CTA */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-white/[0.02] border-y border-white/5">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6 }}
          className="max-w-3xl mx-auto text-center"
        >
          <h2 className="text-2xl font-bold text-white mb-4">{t("pricing.faq.title")}</h2>
          <p className="text-gray-400 mb-6">{t("pricing.faq.subtitle")}</p>
          <a
            href={CAL_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-8 py-3 rounded-xl bg-eko-violet text-white font-semibold hover:bg-eko-violet-dark transition-colors"
          >
            <Zap className="w-4 h-4" />
            {t("pricing.faq.cta")}
          </a>
        </motion.div>
      </section>

      {/* Footer (mirrors home) */}
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
