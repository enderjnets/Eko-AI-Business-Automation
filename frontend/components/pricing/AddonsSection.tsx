"use client";

import { motion } from "framer-motion";
import { Palette, Phone, Plug, Server } from "lucide-react";
import { useT } from "@/contexts/I18nProvider";

const ADDONS = [
  { id: "whitelabel", Icon: Palette, color: "text-eko-magenta" },
  { id: "whatsapp", Icon: Phone, color: "text-eko-green" },
  { id: "integration", Icon: Plug, color: "text-eko-violet" },
  { id: "onprem", Icon: Server, color: "text-gold" },
] as const;

export default function AddonsSection() {
  const { t } = useT();
  return (
    <section className="py-16 px-4 sm:px-6 lg:px-8 border-t border-white/5">
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-80px" }}
        transition={{ duration: 0.6 }}
        className="max-w-6xl mx-auto"
      >
        <div className="text-center mb-10">
          <h2 className="text-2xl sm:text-3xl font-bold text-white mb-2">{t("pricing.addons.title")}</h2>
          <p className="text-gray-500 text-sm max-w-xl mx-auto">{t("pricing.addons.subtitle")}</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {ADDONS.map(({ id, Icon, color }) => (
            <div
              key={id}
              className="rounded-2xl border border-white/5 bg-white/[0.02] p-5 hover:border-white/10 transition-colors"
            >
              <Icon className={`w-6 h-6 ${color} mb-3`} aria-hidden />
              <h3 className="text-base font-semibold text-white mb-1">
                {t(`pricing.addons.${id}.name` as never)}
              </h3>
              <p className="text-xs text-gray-500 mb-4 leading-relaxed h-12">
                {t(`pricing.addons.${id}.desc` as never)}
              </p>
              <div className="text-sm font-semibold text-white">
                {t(`pricing.addons.${id}.price` as never)}
              </div>
            </div>
          ))}
        </div>
      </motion.div>
    </section>
  );
}
