"use client";

import { useState } from "react";
import Link from "next/link";
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
  Building2,
  UtensilsCrossed,
  Stethoscope,
  Dumbbell,
  Store,
  Briefcase,
} from "lucide-react";

const INDUSTRIES = [
  { icon: Sparkles, label: "Spas & Salones", desc: "Recepción 24/7, reservas, recordatorios" },
  { icon: UtensilsCrossed, label: "Restaurantes", desc: "Pedidos, reservas, atención al cliente" },
  { icon: Stethoscope, label: "Clínicas & Médicos", desc: "Agendamiento, seguimiento, recordatorios" },
  { icon: Dumbbell, label: "Gimnasios", desc: "Membresías, clases, consultas" },
  { icon: Store, label: "Retail & E-commerce", desc: "Soporte, FAQs, seguimiento de pedidos" },
  { icon: Briefcase, label: "Profesionales", desc: "Abogados, contadores, coaches, agencias" },
];

const FEATURES = [
  {
    icon: Bot,
    title: "Agente IA 24/7",
    desc: "Tu negocio nunca duerme. La IA responde llamadas, emails y chats a cualquier hora.",
  },
  {
    icon: Calendar,
    title: "Agendamiento Automático",
    desc: "Clientes reservan citas directamente con tu calendario. Sin intervención humana.",
  },
  {
    icon: MessageSquare,
    title: "Respuestas Instantáneas",
    desc: "WhatsApp, email, SMS y chat web. Un solo agente para todos los canales.",
  },
  {
    icon: TrendingUp,
    title: "Escalable",
    desc: "Atiende 10 o 1,000 clientes al mismo tiempo. Crece sin contratar más personal.",
  },
  {
    icon: Clock,
    title: "Ahorro de Tiempo",
    desc: "Reduce 15-20 horas semanales de trabajo administrativo y repetitivo.",
  },
  {
    icon: Shield,
    title: "Datos Seguros",
    desc: "Información de clientes protegida. Cumplimiento con estándares de privacidad.",
  },
];

const HOW_IT_WORKS = [
  {
    step: "01",
    title: "Agenda tu Demo",
    desc: "15 minutos para entender tu negocio y mostrarte lo que la IA puede hacer por ti.",
  },
  {
    step: "02",
    title: "Setup en 48h",
    desc: "Configuramos tu agente con tu información, servicios, precios y tono de marca.",
  },
  {
    step: "03",
    title: "Activa y Escala",
    desc: "Tu agente IA atiende clientes, agenda citas y libera tu tiempo desde el día 1.",
  },
];

export default function LandingPage() {
  const [form, setForm] = useState({
    business_name: "",
    email: "",
    phone: "",
    category: "",
  });
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

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
          notes: `Lead capturado desde landing page. Industria: ${form.category || "No especificada"}`,
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
            <a href="#como-funciona" className="text-sm text-gray-400 hover:text-white transition-colors">Cómo funciona</a>
            <a href="#industrias" className="text-sm text-gray-400 hover:text-white transition-colors">Industrias</a>
            <Link href="/pricing" className="text-sm text-gray-400 hover:text-white transition-colors">Precios</Link>
            <a href="https://cal.com/ender-ocando-lfxtkn/15min" target="_blank" rel="noopener noreferrer" className="text-sm px-4 py-2 rounded-lg bg-eko-blue text-white font-medium hover:bg-eko-blue-dark transition-colors">
              Agenda tu Demo
            </a>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-eko-blue/10 border border-eko-blue/20 text-eko-blue text-xs font-medium mb-6">
            <Sparkles className="w-3.5 h-3.5" />
            Automatización con Inteligencia Artificial para cualquier negocio
          </div>
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold font-display text-white leading-tight mb-6">
            Tu negocio funciona{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-eko-blue to-cyan-400">
              mientras duermes
            </span>
          </h1>
          <p className="text-lg sm:text-xl text-gray-400 max-w-2xl mx-auto mb-10 leading-relaxed">
            Agente IA que atiende clientes, agenda citas, responde preguntas y sigue leads —{" "}
            <span className="text-white font-medium">24/7, en todos tus canales</span>. Reduce costos, elimina tareas repetitivas y escala sin contratar más personal.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
            <Link
              href="https://cal.com/ender-ocando-lfxtkn/15min"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-eko-blue text-white font-semibold hover:bg-eko-blue-dark transition-all flex items-center justify-center gap-2"
            >
              <Calendar className="w-5 h-5" />
              Agenda tu Demo Gratis
            </Link>
            <Link
              href="/pricing"
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-white/5 border border-white/10 text-white font-semibold hover:bg-white/10 transition-all flex items-center justify-center gap-2"
            >
              Ver Precios
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>

          {/* Social Proof */}
          <div className="flex flex-wrap items-center justify-center gap-8 text-gray-500 text-sm">
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-eko-green" />
              <span>Setup en 48 horas</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-eko-green" />
              <span>Sin contratos de permanencia</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-eko-green" />
              <span>Cancela cuando quieras</span>
            </div>
          </div>
        </div>
      </section>

      {/* Lead Capture Form */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-white/[0.02] border-y border-white/5">
        <div className="max-w-xl mx-auto">
          {submitted ? (
            <div className="text-center py-8">
              <CheckCircle className="w-14 h-14 text-eko-green mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-white mb-2">¡Gracias por tu interés!</h2>
              <p className="text-gray-400 mb-4">
                Hemos recibido tu información. Nuestro equipo te contactará en menos de 24 horas.
              </p>
              <a href="https://cal.com/ender-ocando-lfxtkn/15min" target="_blank" rel="noopener noreferrer" className="text-eko-blue hover:underline text-sm">
                O agenda tu demo ahora →
              </a>
            </div>
          ) : (
            <>
              <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-white mb-2">¿Quieres saber cuánto puedes ahorrar?</h2>
                <p className="text-gray-400 text-sm">
                  Déjanos tus datos y te enviamos un análisis gratuito de automatización para tu negocio.
                </p>
              </div>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <input
                    type="text"
                    required
                    placeholder="Nombre de tu negocio"
                    value={form.business_name}
                    onChange={(e) => setForm({ ...form, business_name: e.target.value })}
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-eko-blue text-sm"
                  />
                  <select
                    value={form.category}
                    onChange={(e) => setForm({ ...form, category: e.target.value })}
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-eko-blue text-sm appearance-none"
                  >
                    <option value="" className="bg-eko-graphite text-gray-500">Tipo de negocio</option>
                    <option value="Spa / Salón" className="bg-eko-graphite">Spa / Salón</option>
                    <option value="Restaurante / Bar" className="bg-eko-graphite">Restaurante / Bar</option>
                    <option value="Clínica / Médico" className="bg-eko-graphite">Clínica / Médico</option>
                    <option value="Gimnasio / Fitness" className="bg-eko-graphite">Gimnasio / Fitness</option>
                    <option value="Retail / Tienda" className="bg-eko-graphite">Retail / Tienda</option>
                    <option value="Profesional Independiente" className="bg-eko-graphite">Profesional Independiente</option>
                    <option value="Otro" className="bg-eko-graphite">Otro</option>
                  </select>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <input
                    type="email"
                    placeholder="Email"
                    value={form.email}
                    onChange={(e) => setForm({ ...form, email: e.target.value })}
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-eko-blue text-sm"
                  />
                  <input
                    type="tel"
                    placeholder="Teléfono (opcional)"
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
                      Enviando...
                    </>
                  ) : (
                    <>
                      <Zap className="w-4 h-4" />
                      Recibir Análisis Gratis
                    </>
                  )}
                </button>
                <p className="text-center text-gray-600 text-xs">
                  Sin spam. Solo te contactaremos sobre tu análisis de automatización.
                </p>
              </form>
            </>
          )}
        </div>
      </section>

      {/* Industries */}
      <section id="industrias" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white mb-3">Para cualquier tipo de negocio</h2>
            <p className="text-gray-400 max-w-xl mx-auto">
              Desde spas hasta agencias de marketing. Si tu negocio interactúa con clientes, la IA puede automatizarlo.
            </p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {INDUSTRIES.map((ind) => (
              <div
                key={ind.label}
                className="group p-6 rounded-xl border border-white/5 bg-white/[0.02] hover:bg-white/5 hover:border-white/10 transition-all"
              >
                <div className="w-10 h-10 rounded-lg bg-eko-blue/10 flex items-center justify-center mb-4 group-hover:bg-eko-blue/20 transition-colors">
                  <ind.icon className="w-5 h-5 text-eko-blue" />
                </div>
                <h3 className="text-white font-semibold mb-1">{ind.label}</h3>
                <p className="text-gray-500 text-sm">{ind.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white/[0.02] border-y border-white/5">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white mb-3">Todo lo que tu agente IA hace por ti</h2>
            <p className="text-gray-400 max-w-xl mx-auto">
              Un solo sistema que reemplaza a múltiples herramientas y horas de trabajo manual.
            </p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {FEATURES.map((feat) => (
              <div key={feat.title} className="p-6 rounded-xl">
                <div className="w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center mb-4">
                  <feat.icon className="w-5 h-5 text-eko-blue" />
                </div>
                <h3 className="text-white font-semibold mb-2">{feat.title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{feat.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it Works */}
      <section id="como-funciona" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white mb-3">De la demo a la activación en 3 pasos</h2>
            <p className="text-gray-400 max-w-xl mx-auto">
              Sin complicaciones técnicas. Nosotros hacemos todo el trabajo pesado.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {HOW_IT_WORKS.map((step) => (
              <div key={step.step} className="text-center">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-eko-blue to-eko-blue-dark flex items-center justify-center mx-auto mb-5">
                  <span className="text-white font-bold text-lg">{step.step}</span>
                </div>
                <h3 className="text-white font-semibold text-lg mb-2">{step.title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-eko-blue/5 to-transparent">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            ¿Listo para automatizar tu negocio?
          </h2>
          <p className="text-gray-400 text-lg mb-8">
            Agenda una demo de 15 minutos. Sin compromiso. Te mostramos exactamente cómo la IA funcionará en tu negocio.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href="https://cal.com/ender-ocando-lfxtkn/15min"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-8 py-4 rounded-xl bg-eko-blue text-white font-semibold hover:bg-eko-blue-dark transition-all flex items-center justify-center gap-2 text-lg"
            >
              <Calendar className="w-5 h-5" />
              Agendar Demo Gratis
            </Link>
            <Link
              href="/pricing"
              className="w-full sm:w-auto px-8 py-4 rounded-xl bg-white/5 border border-white/10 text-white font-semibold hover:bg-white/10 transition-all"
            >
              Ver Planes y Precios
            </Link>
          </div>
        </div>
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
            © {new Date().getFullYear()} Eko AI Automation. Todos los derechos reservados.
          </p>
          <div className="flex items-center gap-4 text-sm text-gray-500">
            <a href="mailto:contact@biz.ekoaiautomation.com" className="hover:text-gray-300 transition-colors">
              contact@biz.ekoaiautomation.com
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
