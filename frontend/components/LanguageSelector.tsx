"use client";

import { useEffect, useRef, useState } from "react";
import { Languages, Check } from "lucide-react";
import { useT } from "@/contexts/I18nProvider";

const FLAGS: Record<"en" | "es", string> = {
  en: "🇺🇸",
  es: "🇪🇸",
};

export default function LanguageSelector() {
  const { lang, setLang, t } = useT();
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const onDoc = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    };
    if (open) document.addEventListener("mousedown", onDoc);
    return () => document.removeEventListener("mousedown", onDoc);
  }, [open]);

  return (
    <div ref={ref} className="relative">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-gray-300 hover:text-white text-xs font-medium transition-colors"
        title={t("lang.switch")}
        aria-haspopup="listbox"
        aria-expanded={open}
      >
        <Languages className="w-3.5 h-3.5" />
        <span>{FLAGS[lang]}</span>
        <span className="hidden sm:inline">{lang.toUpperCase()}</span>
      </button>

      {open && (
        <div
          role="listbox"
          className="absolute right-0 top-full mt-1.5 min-w-[140px] rounded-lg border border-white/10 bg-eko-graphite/95 backdrop-blur shadow-xl z-50 overflow-hidden animate-fade-in"
        >
          {(["en", "es"] as const).map((l) => (
            <button
              key={l}
              type="button"
              role="option"
              aria-selected={l === lang}
              onClick={() => {
                setLang(l);
                setOpen(false);
              }}
              className={`w-full flex items-center justify-between gap-2 px-3 py-2 text-sm hover:bg-white/5 transition-colors ${
                l === lang ? "text-white" : "text-gray-300"
              }`}
            >
              <span className="flex items-center gap-2">
                <span className="text-base leading-none">{FLAGS[l]}</span>
                {t(`lang.label.${l}` as any)}
              </span>
              {l === lang && <Check className="w-3.5 h-3.5 text-eko-green" />}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
