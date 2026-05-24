"use client";

import { useMemo, useState } from "react";
import { Calculator, TrendingUp } from "lucide-react";
import { useT } from "@/contexts/I18nProvider";

const RATES = [30, 60, 100, 150] as const;
const RATE_LABEL_KEYS: Record<(typeof RATES)[number], string> = {
  30: "pricing.roi.rate_30",
  60: "pricing.roi.rate_60",
  100: "pricing.roi.rate_100",
  150: "pricing.roi.rate_150",
};

const GROWTH_PRICE_USD = 749;
const MAX_HOURS = 200;

const formatUSD = (n: number) =>
  new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(n);

export default function ROICalculator() {
  const { t } = useT();
  const [hoursRaw, setHoursRaw] = useState<string>("20");
  const [rate, setRate] = useState<(typeof RATES)[number]>(60);

  const { savings, ratio } = useMemo(() => {
    const parsed = parseInt(hoursRaw, 10);
    const hours = Number.isFinite(parsed) ? Math.min(Math.max(parsed, 0), MAX_HOURS) : 0;
    const s = hours * rate;
    const r = s / GROWTH_PRICE_USD;
    return { savings: s, ratio: r };
  }, [hoursRaw, rate]);

  return (
    <div className="max-w-3xl mx-auto rounded-2xl border border-white/10 bg-gradient-to-b from-eko-violet/5 to-transparent p-6 sm:p-8">
      <div className="flex items-center gap-2 mb-2 text-eko-violet">
        <Calculator className="w-5 h-5" />
        <span className="text-xs font-medium uppercase tracking-wider">{t("pricing.roi.title")}</span>
      </div>
      <h3 className="text-2xl sm:text-3xl font-bold text-white mb-2">{t("pricing.roi.title")}</h3>
      <p className="text-gray-400 text-sm mb-6">{t("pricing.roi.subtitle")}</p>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
        <label className="block">
          <span className="text-xs text-gray-500 mb-1.5 block">{t("pricing.roi.hours_label")}</span>
          <input
            type="number"
            inputMode="numeric"
            min={0}
            max={MAX_HOURS}
            value={hoursRaw}
            onChange={(e) => setHoursRaw(e.target.value)}
            className="w-full px-4 py-2.5 rounded-lg bg-white/5 border border-white/10 text-white text-lg font-semibold focus:outline-none focus:border-eko-violet/50"
            aria-label={t("pricing.roi.hours_label")}
          />
        </label>
        <label className="block">
          <span className="text-xs text-gray-500 mb-1.5 block">{t("pricing.roi.rate_label")}</span>
          <select
            value={rate}
            onChange={(e) => setRate(Number(e.target.value) as (typeof RATES)[number])}
            className="w-full px-4 py-2.5 rounded-lg bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-eko-violet/50"
            aria-label={t("pricing.roi.rate_label")}
          >
            {RATES.map((r) => (
              <option key={r} value={r} className="bg-eko-noir">
                {t(RATE_LABEL_KEYS[r] as never)}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div className="rounded-xl bg-white/[0.03] border border-white/5 p-5">
          <div className="text-[10px] uppercase tracking-wider text-gray-500 mb-1">
            {t("pricing.roi.savings_label")}
          </div>
          <div className="text-3xl font-bold text-eko-green">
            {savings > 0 ? formatUSD(savings) : "—"}
          </div>
        </div>
        <div className="rounded-xl bg-white/[0.03] border border-white/5 p-5">
          <div className="text-[10px] uppercase tracking-wider text-gray-500 mb-1">
            {t("pricing.roi.vs_label")}
          </div>
          <div className="text-3xl font-bold text-white inline-flex items-center gap-1.5">
            {ratio > 0 ? (
              <>
                {ratio.toFixed(1)}
                <TrendingUp className="w-5 h-5 text-eko-green" />
              </>
            ) : (
              "—"
            )}
            {ratio > 0 && (
              <span className="text-xs font-normal text-gray-500 ml-1">{t("pricing.roi.x_times")}</span>
            )}
          </div>
        </div>
      </div>

      <p className="text-xs text-gray-500 mt-4 italic">{t("pricing.roi.hint")}</p>
    </div>
  );
}
