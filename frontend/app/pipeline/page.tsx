"use client";

import Navbar from "@/components/Navbar";
import KanbanBoard from "@/components/KanbanBoard";
import { useT } from "@/contexts/I18nProvider";

export default function PipelinePage() {
  const { t } = useT();
  return (
    <div className="min-h-screen bg-eko-graphite">
      <Navbar />
      <main className="pt-20 pb-12 px-4 sm:px-6 lg:px-8 max-w-[1600px] mx-auto">
        <div className="mb-6">
          <h1 className="text-2xl font-bold font-display">{t("pipeline.title")}</h1>
          <p className="text-gray-400 text-sm mt-1">
            {t("pipeline.subtitle")}
          </p>
        </div>

        <KanbanBoard />
      </main>
    </div>
  );
}
