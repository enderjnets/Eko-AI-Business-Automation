"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import axios from "axios";
import { useT } from "@/contexts/I18nProvider";
import {
  Loader2,
  CreditCard,
  Calendar,
  CheckCircle,
  AlertTriangle,
  XCircle,
  ArrowRight,
  Shield,
  Receipt,
  ExternalLink,
} from "lucide-react";

interface Payment {
  id: number;
  type: string;
  status: string;
  amount_cents: number;
  currency: string;
  paid_at: string | null;
  billing_period_start: string | null;
  billing_period_end: string | null;
  receipt_url: string | null;
  meta: any;
}

interface SubscriptionInfo {
  id: string;
  status: string;
  current_period_start: number;
  current_period_end: number;
  cancel_at_period_end: boolean;
  plan: string | null;
}

interface BillingInfo {
  lead_id: number;
  business_name: string | null;
  email: string | null;
  plan: string | null;
  subscription_status: string | null;
  stripe_customer_id: string | null;
  payments: Payment[];
  subscription: SubscriptionInfo | null;
}

function BillingPageInner() {
  const searchParams = useSearchParams();
  const leadId = searchParams.get("lead_id");
  const [data, setData] = useState<BillingInfo | null>(null);
  const { t } = useT();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [portalLoading, setPortalLoading] = useState(false);

  const STATUS_STYLES: Record<string, { icon: React.ReactNode; color: string; label: string }> = {
    active: { icon: <CheckCircle className="w-4 h-4" />, color: "text-green-600 bg-green-50 border-green-200", label: t("billing.status.active") },
    past_due: { icon: <AlertTriangle className="w-4 h-4" />, color: "text-yellow-600 bg-yellow-50 border-yellow-200", label: t("billing.status.past_due") },
    canceled: { icon: <XCircle className="w-4 h-4" />, color: "text-red-600 bg-red-50 border-red-200", label: t("billing.status.canceled") },
    canceling: { icon: <AlertTriangle className="w-4 h-4" />, color: "text-orange-600 bg-orange-50 border-orange-200", label: t("billing.status.canceling") },
    inactive: { icon: <XCircle className="w-4 h-4" />, color: "text-gray-600 bg-gray-50 border-gray-200", label: t("billing.status.inactive") },
  };

  useEffect(() => {
    if (leadId) {
      loadBilling();
    } else {
      setLoading(false);
      setError(t("billing.error.no_customer"));
    }
  }, [leadId]);

  async function loadBilling() {
    try {
      const res = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL || ""}/api/v1/checkout/billing/${leadId}`
      );
      setData(res.data);
    } catch (e: any) {
      setError(e.response?.data?.detail || t("billing.error.load"));
    } finally {
      setLoading(false);
    }
  }

  async function openPortal() {
    if (!leadId) return;
    setPortalLoading(true);
    try {
      const res = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL || ""}/api/v1/checkout/portal`,
        {
          lead_id: parseInt(leadId),
          return_url: `${typeof window !== "undefined" ? window.location.origin : ""}/billing?lead_id=${leadId}`,
        }
      );
      if (res.data.portal_url) {
        window.location.href = res.data.portal_url;
      }
    } catch (e: any) {
      setError(e.response?.data?.detail || t("billing.error.portal"));
    } finally {
      setPortalLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Loader2 className="w-10 h-10 animate-spin text-blue-600" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
        <div className="text-center max-w-md">
          <AlertTriangle className="w-12 h-12 text-yellow-500 mx-auto mb-4" />
          <h1 className="text-xl font-bold text-gray-900 mb-2">{t("billing.error.title")}</h1>
          <p className="text-gray-600">{error}</p>
        </div>
      </div>
    );
  }

  if (!data) return null;

  const status = data.subscription_status || "inactive";
  const statusStyle = STATUS_STYLES[status] || STATUS_STYLES.inactive;
  const nextBillingDate = data.subscription?.current_period_end
    ? new Date(data.subscription.current_period_end * 1000).toLocaleDateString("es-MX", {
        year: "numeric",
        month: "long",
        day: "numeric",
      })
    : null;

  const planNames: Record<string, string> = {
    starter: "Eko AI Starter",
    growth: "Eko AI Growth",
    enterprise: "Eko AI Enterprise",
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-3xl mx-auto px-4 py-6">
          <div className="flex items-center gap-2 mb-1">
            <CreditCard className="w-5 h-5 text-blue-600" />
            <h1 className="text-xl font-bold text-gray-900">{t("billing.title")}</h1>
          </div>
          <p className="text-gray-500 text-sm">
            {data.business_name || data.email || t("billing.customer")}
          </p>
        </div>
      </div>

      <div className="max-w-3xl mx-auto px-4 py-8 space-y-6">
        {/* Status Card */}
        <div className={`rounded-xl border p-5 ${statusStyle.color}`}>
          <div className="flex items-center gap-2 mb-2">
            {statusStyle.icon}
            <span className="font-semibold">{statusStyle.label}</span>
          </div>
          <p className="text-sm opacity-90">
            {t("billing.plan_label")}: <strong>{planNames[data.plan || ""] || data.plan || "—"}</strong>
          </p>
          {nextBillingDate && data.subscription_status === "active" && (
            <p className="text-sm opacity-90 mt-1">
              {t("billing.next_charge")}: <strong>{nextBillingDate}</strong>
            </p>
          )}
          {data.subscription?.cancel_at_period_end && (
            <p className="text-sm opacity-90 mt-1">
              {t("billing.cancel_notice")} <strong>{nextBillingDate}</strong>
            </p>
          )}
        </div>

        {/* Actions */}
        {data.stripe_customer_id && (
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <h3 className="font-semibold text-gray-900 mb-3">{t("billing.manage_sub")}</h3>
            <button
              onClick={openPortal}
              disabled={portalLoading}
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
            >
              {portalLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <ExternalLink className="w-4 h-4" />
              )}
              {t("billing.open_portal")}
              <ArrowRight className="w-4 h-4" />
            </button>
            <p className="text-xs text-gray-400 mt-2">
              {t("billing.portal_hint")}
            </p>
          </div>
        )}

        {/* Payment History */}
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <div className="flex items-center gap-2 mb-4">
            <Receipt className="w-5 h-5 text-gray-600" />
            <h3 className="font-semibold text-gray-900">{t("billing.history")}</h3>
          </div>

          {data.payments.length === 0 ? (
            <p className="text-gray-500 text-sm">{t("billing.no_payments")}</p>
          ) : (
            <div className="space-y-3">
              {data.payments.map((p) => (
                <div
                  key={p.id}
                  className="flex items-center justify-between py-3 border-b border-gray-100 last:border-0"
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                        p.status === "completed"
                          ? "bg-green-100 text-green-600"
                          : p.status === "failed"
                          ? "bg-red-100 text-red-600"
                          : "bg-gray-100 text-gray-600"
                      }`}
                    >
                      {p.status === "completed" ? (
                        <CheckCircle className="w-4 h-4" />
                      ) : p.status === "failed" ? (
                        <XCircle className="w-4 h-4" />
                      ) : (
                        <Receipt className="w-4 h-4" />
                      )}
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">
                        {p.type === "setup"
                          ? t("billing.type.setup")
                          : p.type === "subscription"
                          ? t("billing.type.subscription")
                          : t("billing.type.payment")}
                      </p>
                      <p className="text-xs text-gray-500">
                        {p.paid_at
                          ? new Date(p.paid_at).toLocaleDateString("es-MX")
                          : t("billing.pending")}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-semibold text-gray-900">
                      ${(p.amount_cents / 100).toFixed(2)}
                    </p>
                    <p className="text-xs text-gray-500 uppercase">{p.currency}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Security Footer */}
        <div className="flex items-center justify-center gap-2 text-xs text-gray-400">
          <Shield className="w-3 h-3" />
          <span>{t("billing.secure_footer")}</span>
        </div>
      </div>
    </div>
  );
}

export default function BillingPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <Loader2 className="w-10 h-10 animate-spin text-blue-600" />
        </div>
      }
    >
      <BillingPageInner />
    </Suspense>
  );
}
