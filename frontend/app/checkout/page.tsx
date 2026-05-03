"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import axios from "axios";
import {
  Loader2,
  CheckCircle,
  Zap,
  TrendingUp,
  Building2,
  Shield,
} from "lucide-react";

interface Plan {
  key: string;
  name: string;
  monthly: number;
  setup: number;
  features: string[];
  icon: React.ReactNode;
  recommended?: boolean;
}

const PLANS: Plan[] = [
  {
    key: "starter",
    name: "Starter",
    monthly: 199,
    setup: 499,
    features: [
      "1 Agente IA personalizado",
      "Horario comercial (8am–6pm)",
      "Respuestas en Español/Inglés",
      "Agendamiento automático",
      "Soporte por email",
    ],
    icon: <Zap className="w-5 h-5" />,
  },
  {
    key: "growth",
    name: "Growth",
    monthly: 299,
    setup: 499,
    features: [
      "2 Agentes IA personalizados",
      "Horario extendido (7am–9pm)",
      "Respuestas en Español/Inglés",
      "Agendamiento + seguimiento automático",
      "Soporte prioritario",
      "Dashboard de analytics",
    ],
    icon: <TrendingUp className="w-5 h-5" />,
    recommended: true,
  },
  {
    key: "enterprise",
    name: "Enterprise",
    monthly: 399,
    setup: 499,
    features: [
      "Agentes IA ilimitados",
      "24/7 — siempre disponible",
      "Respuestas en Español/Inglés",
      "Agendamiento + seguimiento + CRM",
      "Soporte dedicado",
      "API access + webhooks",
      "Custom integrations",
    ],
    icon: <Building2 className="w-5 h-5" />,
  },
];

function CheckoutPageInner() {
  const searchParams = useSearchParams();
  const leadId = searchParams.get("lead_id");
  const [selectedPlan, setSelectedPlan] = useState<string>("growth");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!leadId) {
      setError("No se encontró información del cliente. Por favor contacta a soporte.");
    }
  }, [leadId]);

  async function handleCheckout(planKey: string) {
    if (!leadId) return;
    setLoading(true);
    setError("");
    try {
      const res = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL || ""}/api/v1/checkout/session`,
        {
          lead_id: parseInt(leadId),
          plan: planKey,
          success_url: `${typeof window !== "undefined" ? window.location.origin : ""}/checkout/success`,
          cancel_url: `${typeof window !== "undefined" ? window.location.origin : ""}/checkout`,
        }
      );
      if (res.data.checkout_url) {
        window.location.href = res.data.checkout_url;
      }
    } catch (e: any) {
      setError(e.response?.data?.detail || "Error iniciando el pago. Intenta de nuevo.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-5xl mx-auto px-4 py-6">
          <div className="flex items-center gap-2">
            <Shield className="w-6 h-6 text-blue-600" />
            <h1 className="text-xl font-bold text-gray-900">Finalizar suscripción</h1>
          </div>
          <p className="text-gray-500 text-sm mt-1">
            Suscripción mensual con setup único. Cancela cuando quieras.
          </p>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 py-10">
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm">
            {error}
          </div>
        )}

        {/* Security badge */}
        <div className="flex items-center justify-center gap-2 mb-8 text-sm text-gray-500">
          <Shield className="w-4 h-4 text-green-500" />
          <span>Pago seguro procesado por Stripe</span>
          <span className="mx-2">·</span>
          <span>SSL encriptado</span>
        </div>

        {/* Plans */}
        <div className="grid md:grid-cols-3 gap-6">
          {PLANS.map((plan) => {
            const isSelected = selectedPlan === plan.key;
            const total = plan.monthly + plan.setup;
            return (
              <div
                key={plan.key}
                onClick={() => setSelectedPlan(plan.key)}
                className={`relative rounded-xl border-2 p-6 cursor-pointer transition-all ${
                  isSelected
                    ? "border-blue-600 bg-blue-50/50 shadow-md"
                    : "border-gray-200 bg-white hover:border-gray-300"
                }`}
              >
                {plan.recommended && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-blue-600 text-white text-xs font-semibold px-3 py-1 rounded-full">
                    Recomendado
                  </div>
                )}

                <div className="flex items-center gap-2 mb-4">
                  <div className={`p-2 rounded-lg ${isSelected ? "bg-blue-100 text-blue-600" : "bg-gray-100 text-gray-600"}`}>
                    {plan.icon}
                  </div>
                  <h3 className="font-bold text-gray-900">{plan.name}</h3>
                </div>

                <div className="mb-4">
                  <div className="flex items-baseline gap-1">
                    <span className="text-3xl font-bold text-gray-900">
                      ${plan.monthly}
                    </span>
                    <span className="text-gray-500">/mes</span>
                  </div>
                  <p className="text-sm text-gray-500 mt-1">
                    + ${plan.setup} setup único
                  </p>
                </div>

                <ul className="space-y-2 mb-6">
                  {plan.features.map((f, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-gray-600">
                      <CheckCircle className="w-4 h-4 text-green-500 mt-0.5 shrink-0" />
                      {f}
                    </li>
                  ))}
                </ul>

                <div className="text-center">
                  <p className="text-xs text-gray-400 mb-2">
                    Total hoy: <strong className="text-gray-700">${total}</strong>
                  </p>
                </div>
              </div>
            );
          })}
        </div>

        {/* CTA */}
        <div className="mt-10 text-center">
          <button
            onClick={() => handleCheckout(selectedPlan)}
            disabled={loading || !leadId}
            className="inline-flex items-center gap-2 px-8 py-4 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-lg"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Redirigiendo a Stripe...
              </>
            ) : (
              <>
                <Shield className="w-5 h-5" />
                Pagar con Stripe — $
                {PLANS.find((p) => p.key === selectedPlan)!.monthly +
                  PLANS.find((p) => p.key === selectedPlan)!.setup}
              </>
            )}
          </button>
          <p className="text-xs text-gray-400 mt-3">
            Se te redirigirá a Stripe para completar el pago de forma segura.
          </p>
        </div>
      </div>
    </div>
  );
}

export default function CheckoutPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <Loader2 className="w-10 h-10 animate-spin text-blue-600" />
        </div>
      }
    >
      <CheckoutPageInner />
    </Suspense>
  );
}
