"use client";

import { useState } from "react";
import { Briefcase, Check, Home, FileText } from "lucide-react";
import { useT } from "@/contexts/I18nProvider";

type Vertical = "accounting" | "realestate" | "legalhealth";

const VERTICALS: { id: Vertical; Icon: typeof Briefcase }[] = [
  { id: "accounting", Icon: Briefcase },
  { id: "realestate", Icon: Home },
  { id: "legalhealth", Icon: FileText },
];

const VERTICAL_FEATURE_COUNT = 5;

export default function GrowthVerticalTabs() {
  const { t } = useT();
  const [active, setActive] = useState<Vertical>("accounting");

  const verticalKeys = Array.from({ length: VERTICAL_FEATURE_COUNT }, (_, i) => `pricing.growth.${active}.f${i + 1}`);

  return (
    <div className="mt-4 mb-4">
      <div role="tablist" className="flex flex-wrap gap-1.5 mb-3" aria-label="Growth vertical">
        {VERTICALS.map(({ id, Icon }) => (
          <button
            key={id}
            type="button"
            role="tab"
            aria-selected={active === id}
            onClick={() => setActive(id)}
            className={`flex-1 min-w-[100px] px-3 py-2 rounded-lg text-xs font-medium inline-flex items-center justify-center gap-1.5 transition-all ${
              active === id
                ? "bg-eko-violet/20 text-white border border-eko-violet/40"
                : "bg-white/[0.03] text-gray-400 border border-white/5 hover:text-white hover:bg-white/5"
            }`}
          >
            <Icon className="w-3.5 h-3.5" aria-hidden />
            <span>{t(`pricing.growth.tab.${id}` as never)}</span>
          </button>
        ))}
      </div>
      <p className="text-[10px] text-gray-500 mb-3 italic">{t("pricing.growth.tab_subtitle")}</p>

      <ul className="space-y-2.5">
        {verticalKeys.map((key) => (
          <li key={key} className="flex items-start gap-2.5">
            <Check className="w-4 h-4 text-eko-magenta shrink-0 mt-0.5" aria-hidden />
            <span className="text-gray-300 text-sm">{t(key as never)}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
