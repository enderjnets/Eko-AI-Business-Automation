"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import axios from "axios";
import {
  CheckCircle,
  Loader2,
  Mail,
  Calendar,
  MessageCircle,
  ArrowRight,
} from "lucide-react";

function CheckoutSuccessPageInner() {
  const searchParams = useSearchParams();
  const sessionId = searchParams.get("session_id");
  const [sessionData, setSessionData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (sessionId) {
      verifySession();
    } else {
      setLoading(false);
      setError("No se encontró información de la sesión de pago.");
    }
  }, [sessionId]);

  async function verifySession() {
    try {
      const res = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL || ""}/api/v1/checkout/session/${sessionId}`
      );
      setSessionData(res.data);
    } catch (e: any) {
      setError(e.response?.data?.detail || "Error verificando el pago.");
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-10 h-10 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">Verificando tu pago...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto px-4">
          <div className="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Mail className="w-8 h-8 text-yellow-600" />
          </div>
          <h2 className="text-xl font-bold text-gray-900 mb-2">
            Estamos verificando tu pago
          </h2>
          <p className="text-gray-600 mb-4">
            {error} No te preocupes — si el pago fue procesado, recibirás un email
            de confirmación en breve.
          </p>
          <p className="text-sm text-gray-400">
            ¿Necesitas ayuda? Escríbenos a{" "}
            <a href="mailto:contact@biz.ekoaiautomation.com" className="text-blue-600 underline">
              contact@biz.ekoaiautomation.com
            </a>
          </p>
        </div>
      </div>
    );
  }

  const total = sessionData?.amount_total
    ? `$${(sessionData.amount_total / 100).toFixed(2)}`
    : null;

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="max-w-lg w-full">
        <div className="text-center mb-8">
          <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <CheckCircle className="w-10 h-10 text-green-600" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            ¡Bienvenido a Eko AI!
          </h1>
          <p className="text-gray-600">
            Tu pago fue procesado exitosamente. Recibirás un email de confirmación
            con los siguientes pasos.
          </p>
          {total && (
            <p className="text-sm text-gray-500 mt-2">
              Monto pagado: <strong className="text-gray-700">{total}</strong>
            </p>
          )}
        </div>

        {/* Next steps */}
        <div className="bg-white rounded-xl border border-gray-200 p-6 mb-6">
          <h3 className="font-semibold text-gray-900 mb-4">¿Qué sigue?</h3>
          <div className="space-y-4">
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center shrink-0">
                <Mail className="w-4 h-4 text-blue-600" />
              </div>
              <div>
                <p className="font-medium text-gray-900 text-sm">Email de bienvenida</p>
                <p className="text-gray-500 text-sm">
                  Te enviaremos un email con todos los detalles de tu plan y acceso.
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center shrink-0">
                <Calendar className="w-4 h-4 text-blue-600" />
              </div>
              <div>
                <p className="font-medium text-gray-900 text-sm">Llamada de setup</p>
                <p className="text-gray-500 text-sm">
                  Nuestro equipo te contactará en las próximas 48 horas para agendar
                  la implementación.
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center shrink-0">
                <MessageCircle className="w-4 h-4 text-blue-600" />
              </div>
              <div>
                <p className="font-medium text-gray-900 text-sm">Tu agente IA en vivo</p>
                <p className="text-gray-500 text-sm">
                  En 3–5 días hábiles tu agente IA estará atendiendo llamadas y
                  mensajes por ti.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="text-center">
          <a
            href="mailto:contact@biz.ekoaiautomation.com"
            className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white font-medium rounded-xl hover:bg-blue-700 transition-colors"
          >
            Contactar a soporte
            <ArrowRight className="w-4 h-4" />
          </a>
          <p className="text-xs text-gray-400 mt-3">
            ¿Preguntas? Escríbenos a{" "}
            <a href="mailto:contact@biz.ekoaiautomation.com" className="text-blue-600 underline">
              contact@biz.ekoaiautomation.com
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default function CheckoutSuccessPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <Loader2 className="w-10 h-10 animate-spin text-blue-600" />
        </div>
      }
    >
      <CheckoutSuccessPageInner />
    </Suspense>
  );
}
