"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import {
  Zap,
  Bot,
  Phone,
  Mail,
  Wand2,
  Target,
  GitBranch,
  ArrowRight,
} from "lucide-react";
import { SplineScene } from "@/components/ui/splite";
import { GlowCard } from "@/components/ui/spotlight-card";

const FEATURES = [
  {
    icon: Bot,
    glow: "blue" as const,
    title: "Recepcionista IA 24/7",
    body: "Atiende a tus clientes en cualquier hora, agenda citas, responde preguntas y captura leads — sin contratar más personal.",
  },
  {
    icon: Phone,
    glow: "purple" as const,
    title: "Voice Agent",
    body: "Agentes telefónicos con voz natural que califican prospectos y reservan demos automáticamente.",
  },
  {
    icon: Mail,
    glow: "green" as const,
    title: "Email + SMS Automation",
    body: "Secuencias multi-canal que persiguen leads en piloto automático con personalización basada en IA.",
  },
  {
    icon: Wand2,
    glow: "orange" as const,
    title: "Content Studio",
    body: "Genera videos cortos, landing pages y campañas listos para publicar con un solo prompt.",
  },
  {
    icon: Target,
    glow: "red" as const,
    title: "Lead Qualification",
    body: "Scoring automático de leads basado en signals: industria, intent, presupuesto y fit con tu producto.",
  },
  {
    icon: GitBranch,
    glow: "blue" as const,
    title: "CRM + Pipeline integrado",
    body: "Visualiza el flujo completo desde primer contacto hasta cierre. Sin Zapier, sin integraciones rotas.",
  },
];

// Spline 3D scene "Clarity Stream" (community remix in user workspace).
// Swap by editing spline.design and re-exporting Code → Next.js → Public URI.
const SPLINE_SCENE_URL =
  "https://prod.spline.design/xIPmqKDfIQYkVvEv/scene.splinecode";

export default function ComingSoon() {
  return (
    <div className="min-h-screen bg-eko-graphite text-eko-white">
      {/* Top nav */}
      <nav className="relative z-10 max-w-7xl mx-auto flex items-center justify-between px-6 py-6">
        <Link href="/" className="flex items-center gap-2">
          <div className="bg-eko-blue rounded-lg p-1.5">
            <Zap className="w-5 h-5 text-white" fill="white" />
          </div>
          <span className="font-display font-bold text-xl">
            Eko <span className="text-eko-blue">AI</span>
          </span>
        </Link>
        <div className="hidden md:flex items-center gap-8 text-sm text-gray-300">
          <a href="#features" className="hover:text-white transition-colors">
            Features
          </a>
          <a href="#cta" className="hover:text-white transition-colors">
            Demo
          </a>
          <Link
            href="https://app.ekoaiautomation.com/login"
            className="hover:text-white transition-colors"
          >
            Sign in
          </Link>
        </div>
        <Link
          href="#cta"
          className="hidden sm:inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-eko-blue hover:bg-eko-blue-dark transition-colors text-sm font-medium"
        >
          Book a demo <ArrowRight className="w-4 h-4" />
        </Link>
      </nav>

      {/* Hero — Splite 3D scene + headline */}
      <section className="relative max-w-7xl mx-auto px-6 pt-8 pb-24 md:pt-16 md:pb-32 overflow-hidden">
        {/* Ambient glow */}
        <div
          aria-hidden
          className="absolute inset-0 -z-10 pointer-events-none"
        >
          <div className="absolute top-1/2 left-1/4 -translate-x-1/2 -translate-y-1/2 w-[42rem] h-[42rem] rounded-full bg-eko-blue/20 blur-[120px]" />
          <div className="absolute top-1/3 right-1/4 translate-x-1/2 w-[28rem] h-[28rem] rounded-full bg-purple-500/10 blur-[100px]" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center min-h-[600px]">
          {/* Left: copy + CTAs */}
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="relative z-10 space-y-7"
          >
            <span className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-white/10 bg-white/5 backdrop-blur text-xs uppercase tracking-wider text-gray-300">
              <span className="w-2 h-2 rounded-full bg-eko-green animate-pulse" />
              Business Automation con IA
            </span>
            <h1 className="font-display text-4xl md:text-5xl lg:text-6xl xl:text-7xl font-bold leading-[1.05] tracking-tight">
              Tu negocio funciona
              <br />
              <span className="bg-gradient-to-r from-eko-blue via-cyan-400 to-purple-400 bg-clip-text text-transparent">
                mientras duermes.
              </span>
            </h1>
            <p className="text-lg md:text-xl text-gray-300 max-w-xl leading-relaxed">
              Agentes de IA 24/7 que atienden clientes, agendan citas, califican
              leads y escalan tu operación — sin contratar más personal.
            </p>
            <div className="flex flex-wrap items-center gap-3 pt-2">
              <Link
                href="#cta"
                className="inline-flex items-center gap-2 px-7 py-4 rounded-full bg-eko-blue hover:bg-eko-blue-dark transition-all hover:scale-[1.02] text-base font-semibold shadow-lg shadow-eko-blue/30"
              >
                Agendar demo <ArrowRight className="w-5 h-5" />
              </Link>
              <Link
                href="https://landing.ekoaiautomation.com/"
                className="inline-flex items-center gap-2 px-7 py-4 rounded-full border border-white/15 hover:bg-white/5 transition-colors text-base font-medium"
              >
                Ver en vivo →
              </Link>
            </div>
            <div className="flex items-center gap-8 pt-4 text-xs text-gray-400">
              <div>
                <div className="text-2xl font-bold text-white">24/7</div>
                <div>operación</div>
              </div>
              <div className="h-10 w-px bg-white/10" />
              <div>
                <div className="text-2xl font-bold text-white">0</div>
                <div>código requerido</div>
              </div>
              <div className="h-10 w-px bg-white/10" />
              <div>
                <div className="text-2xl font-bold text-white">5min</div>
                <div>setup</div>
              </div>
            </div>
          </motion.div>

          {/* Right: 3D Spline scene */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 1, delay: 0.2, ease: "easeOut" }}
            className="relative w-full h-[420px] md:h-[560px] lg:h-[600px]"
          >
            <SplineScene
              scene={SPLINE_SCENE_URL}
              className="w-full h-full"
            />
          </motion.div>
        </div>
      </section>

      {/* Features grid with GlowCard spotlight */}
      <section
        id="features"
        className="relative max-w-7xl mx-auto px-6 py-20 md:py-32"
      >
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.7 }}
          className="text-center max-w-3xl mx-auto mb-16"
        >
          <h2 className="font-display text-4xl md:text-5xl font-bold tracking-tight">
            Todo lo que tu negocio necesita,
            <br />
            <span className="text-eko-blue">en una sola plataforma.</span>
          </h2>
          <p className="mt-5 text-lg text-gray-400">
            Sin Zapier, sin integraciones rotas, sin código. Solo IA que trabaja.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {FEATURES.map((f, i) => (
            <motion.div
              key={f.title}
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-50px" }}
              transition={{ duration: 0.5, delay: i * 0.08 }}
            >
              <GlowCard
                glowColor={f.glow}
                customSize
                className="!w-full !h-full min-h-[260px] !p-7 !grid-rows-none flex flex-col gap-4 bg-white/[0.02]"
              >
                <div className="flex items-center gap-3">
                  <div className="p-2.5 rounded-xl bg-white/5 border border-white/10">
                    <f.icon className="w-5 h-5 text-white" />
                  </div>
                </div>
                <h3 className="font-display text-xl font-semibold text-white">
                  {f.title}
                </h3>
                <p className="text-sm text-gray-300 leading-relaxed">{f.body}</p>
              </GlowCard>
            </motion.div>
          ))}
        </div>
      </section>

      {/* CTA section */}
      <section
        id="cta"
        className="relative max-w-5xl mx-auto px-6 py-20 md:py-32 text-center"
      >
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.7 }}
          className="relative rounded-3xl border border-white/10 bg-gradient-to-b from-white/[0.04] to-transparent p-12 md:p-16 overflow-hidden"
        >
          <div
            aria-hidden
            className="absolute -top-1/2 left-1/2 -translate-x-1/2 w-[80%] h-full bg-eko-blue/20 blur-[100px] rounded-full"
          />
          <h2 className="relative font-display text-3xl md:text-5xl font-bold tracking-tight">
            ¿Listo para automatizar tu negocio?
          </h2>
          <p className="relative mt-5 text-lg text-gray-300 max-w-2xl mx-auto">
            Demo gratuita de 15 minutos. Te mostramos exactamente cómo Eko AI
            puede operar tu negocio sin que muevas un dedo.
          </p>
          <div className="relative mt-8 flex flex-wrap items-center justify-center gap-3">
            <Link
              href="https://cal.com/ender-ocando-lfxtkn/15min"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-8 py-4 rounded-full bg-eko-blue hover:bg-eko-blue-dark transition-all hover:scale-[1.02] text-base font-semibold shadow-xl shadow-eko-blue/30"
            >
              Agendar demo gratis <ArrowRight className="w-5 h-5" />
            </Link>
            <Link
              href="https://landing.ekoaiautomation.com/"
              className="inline-flex items-center gap-2 px-8 py-4 rounded-full border border-white/15 hover:bg-white/5 transition-colors text-base font-medium"
            >
              Ver producto en vivo
            </Link>
          </div>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/5">
        <div className="max-w-7xl mx-auto px-6 py-12 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2 text-sm text-gray-400">
            <div className="bg-eko-blue rounded-md p-1">
              <Zap className="w-3.5 h-3.5 text-white" fill="white" />
            </div>
            <span>
              Eko AI Business Automation — Denver, CO
            </span>
          </div>
          <div className="flex items-center gap-6 text-sm text-gray-400">
            <Link
              href="https://app.ekoaiautomation.com/login"
              className="hover:text-white transition-colors"
            >
              Sign in
            </Link>
            <Link
              href="https://landing.ekoaiautomation.com/"
              className="hover:text-white transition-colors"
            >
              Demo
            </Link>
            <a
              href="mailto:hello@biz.ekoaiautomation.com"
              className="hover:text-white transition-colors"
            >
              Contact
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
