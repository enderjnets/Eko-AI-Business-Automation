"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { translations, type Lang, type TranslationKey } from "@/lib/i18n/translations";

interface I18nContextValue {
  lang: Lang;
  setLang: (l: Lang) => void;
  t: (key: TranslationKey, vars?: Record<string, string | number>) => string;
}

const I18nContext = createContext<I18nContextValue | null>(null);

const LS_KEY = "eko_lang_v1";

function detectInitialLang(): Lang {
  if (typeof window === "undefined") return "en";
  try {
    const saved = window.localStorage.getItem(LS_KEY) as Lang | null;
    if (saved === "en" || saved === "es") return saved;
  } catch {
    // ignore
  }
  // Auto-detect from browser, default to English
  const nav = (typeof navigator !== "undefined" && navigator.language) || "";
  if (nav.toLowerCase().startsWith("es")) return "es";
  return "en";
}

export function I18nProvider({ children }: { children: React.ReactNode }) {
  // Always start with "en" on first render to match SSR — then hydrate from
  // localStorage / navigator after mount to avoid React hydration mismatches.
  const [lang, setLangState] = useState<Lang>("en");
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    setLangState(detectInitialLang());
    setHydrated(true);
  }, []);

  useEffect(() => {
    if (!hydrated || typeof window === "undefined") return;
    try {
      window.localStorage.setItem(LS_KEY, lang);
      document.documentElement.setAttribute("lang", lang);
    } catch {
      // ignore
    }
  }, [lang, hydrated]);

  const setLang = useCallback((l: Lang) => setLangState(l), []);

  const t = useCallback(
    (key: TranslationKey, vars?: Record<string, string | number>) => {
      const dict = translations[lang] || translations.en;
      let str = (dict[key] as string) || (translations.en[key] as string) || (key as string);
      if (vars) {
        for (const [k, v] of Object.entries(vars)) {
          str = str.replaceAll(`{${k}}`, String(v));
        }
      }
      return str;
    },
    [lang]
  );

  const value = useMemo(() => ({ lang, setLang, t }), [lang, setLang, t]);

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

export function useT() {
  const ctx = useContext(I18nContext);
  if (!ctx) throw new Error("useT must be used within an I18nProvider");
  return ctx;
}
