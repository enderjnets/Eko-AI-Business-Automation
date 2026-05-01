"use client";

import Link from "next/link";
import { Check, Zap, ArrowRight, Sparkles, Building2 } from "lucide-react";

const PLANS = [
  {
    name: "Starter",
    price: "$199",
    period: "/mes",
    description: "Perfecto para negocios pequeños que reciben hasta 50 consultas/mes.",
    features: [
      "1 Agente IA (voz + chat)",
      "Agendamiento automático",
      "Respuestas por email y SMS",
      "Horario comercial (8h)",
      "Dashboard de métricas básico",
      "Soporte por email",
    ],
    cta: "Agendar Demo",
    href: "/book-demo",
    highlighted: false,
  },
  {
    name: "Growth",
    price: "$299",
    period: "/mes",
    description: "Para negocios en crecimiento con volumen medio de clientes.",
    features: [
      "2 Agentes IA (voz + chat)",
      "Agendamiento + recordatorios",
      "Email, SMS, WhatsApp",
      "Horario extendido (12h)",
      "Dashboard avanzado + reportes",
      "Integración con Calendly/Google",
      "Soporte prioritario",
    ],
    cta: "Agendar Demo",
    href: "/book-demo",
    highlighted: true,
  },
  {
    name: "Enterprise",
    price: "$399",
    period: "/mes",
    description: "Para negocios con alto volumen y necesidades personalizadas.",
    features: [
      "Agentes IA ilimitados",
      "Agendamiento + CRM completo",
      "Todos los canales + API",
      "24/7 sin límites",
      "Analytics + BI personalizado",
      "Integraciones custom",
      "Soporte dedicado",
      "SLA garantizado",
    ],
    cta: "Contactar Ventas",
    href: "/book-demo",
    highlighted: false,
  },
];

export default function PricingPage() {
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
          <div className="flex items-center gap-4">
            <Link href="/" className="text-sm text-gray-400 hover:text-white transition-colors">
              ← Volver
            </Link>
          </div>
        </div>
      </nav>

      {/* Header */}
      <section className="pt-32 pb-12 px-4 sm:px-6 lg:px-8 text-center">
        <div className="max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-eko-blue/10 border border-eko-blue/20 text-eko-blue text-xs font-medium mb-6">
            <Sparkles className="w-3.5 h-3.5" />
            Precios transparentes, sin sorpresas
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold font-display text-white mb-4">
            Un plan para cada negocio
          </h1>
          <p className="text-lg text-gray-400 max-w-xl mx-auto">
            Desde startups hasta empresas consolidadas. Elige el plan que se ajuste a tu volumen y escala cuando crezcas.
          </p>
        </div>
      </section>

      {/* Setup Fee Banner */}
      <section className="pb-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-2xl mx-auto">
          <div className="flex items-center gap-4 p-4 rounded-xl bg-gold/5 border border-gold/20">
            <Building2 className="w-8 h-8 text-gold shrink-0" />
            <div>
              <p className="text-white font-medium">Setup inicial: <span className="text-gold">$499</span></p>
              <p className="text-gray-500 text-sm">
                Incluye configuración completa de tu agente IA, integración con tus sistemas, entrenamiento con tu información de negocio y puesta en marcha.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Cards */}
      <section className="pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
          {PLANS.map((plan) => (
            <div
              key={plan.name}
              className={`relative rounded-2xl border p-8 flex flex-col ${
                plan.highlighted
                  ? "border-eko-blue/30 bg-gradient-to-b from-eko-blue/10 to-transparent"
                  : "border-white/5 bg-white/[0.02]"
              }`}
            >
              {plan.highlighted && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full bg-eko-blue text-white text-xs font-medium">
                  Más popular
                </div>
              )}
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-white mb-2">{plan.name}</h3>
                <div className="flex items-baseline gap-1 mb-3">
                  <span className="text-4xl font-bold text-white">{plan.price}</span>
                  <span className="text-gray-500">{plan.period}</span>
                </div>
                <p className="text-gray-500 text-sm">{plan.description}</p>
              </div>

              <ul className="space-y-3 mb-8 flex-1">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-start gap-3">
                    <Check className="w-4 h-4 text-eko-green shrink-0 mt-0.5" />
                    <span className="text-gray-300 text-sm">{feature}</span>
                  </li>
                ))}
              </ul>

              <Link
                href={plan.href}
                className={`w-full py-3 rounded-xl font-semibold text-center flex items-center justify-center gap-2 transition-all ${
                  plan.highlighted
                    ? "bg-eko-blue text-white hover:bg-eko-blue-dark"
                    : "bg-white/5 border border-white/10 text-white hover:bg-white/10"
                }`}
              >
                {plan.cta}
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          ))}
        </div>
      </section>

      {/* FAQ Teaser */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-white/[0.02] border-y border-white/5">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-2xl font-bold text-white mb-4">¿Tienes dudas?</h2>
          <p className="text-gray-400 mb-6">
            Agenda una demo gratuita de 15 minutos. Te mostramos exactamente cómo funciona la IA en tu tipo de negocio, sin compromiso.
          </p>
          <Link
            href="/book-demo"
            className="inline-flex items-center gap-2 px-8 py-3 rounded-xl bg-eko-blue text-white font-semibold hover:bg-eko-blue-dark transition-colors"
          >
            <Zap className="w-4 h-4" />
            Agendar Demo Gratis
          </Link>
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
        </div>
      </footer>
    </div>
  );
}
