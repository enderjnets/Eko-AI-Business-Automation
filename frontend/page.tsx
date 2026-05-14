"use client";

import { useState } from "react";
import Navbar from "@/components/Navbar";
import PipelineHistory from "@/components/content-studio/PipelineHistory";
import BufferStatus from "@/components/content-studio/BufferStatus";
import StatsPanel from "@/components/content-studio/StatsPanel";
import DataPanel from "@/components/content-studio/DataPanel";
import PostsList from "@/components/content-studio/PostsList";
import {
  Play,
  Activity,
  Database,
  BarChart3,
  Clapperboard,
  Terminal,
  FileText,
  Gauge,
} from "lucide-react";

const TABS = [
  { id: "control", label: "Control", icon: Play },
  { id: "posts", label: "Publicaciones", icon: FileText },
  { id: "monitor", label: "Monitoreo", icon: Activity },
  { id: "data", label: "Datos", icon: Database },
  { id: "stats", label: "Estadísticas", icon: BarChart3 },
];

export default function ContentStudioPage() {
  const [activeTab, setActiveTab] = useState("posts");

  return (
    <div className="min-h-screen bg-eko-graphite">
      <Navbar />

      <main className="pt-20 pb-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 rounded-lg bg-pink-500/10 text-pink-400">
              <Clapperboard className="w-5 h-5" />
            </div>
            <h1 className="text-2xl font-bold font-display">
              Content Studio
            </h1>
          </div>
          <p className="text-gray-400 text-sm">
            Pipeline de producción de contenido para TikTok, Instagram y
            Facebook
          </p>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 mb-6 border-b border-white/5 pb-1 overflow-x-auto">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-t-lg text-sm font-medium transition-colors whitespace-nowrap ${
                activeTab === tab.id
                  ? "text-white bg-white/5 border-b-2 border-pink-400"
                  : "text-gray-500 hover:text-gray-300 hover:bg-white/[0.02]"
              }`}
            >
              <tab.icon className="w-4 h-4" />
              {tab.label}
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="min-h-[400px]">
          {activeTab === "control" && <ControlTab />}
          {activeTab === "posts" && <PostsTab />}
          {activeTab === "monitor" && <MonitorTab />}
          {activeTab === "data" && <DataPanel />}
          {activeTab === "stats" && <StatsPanel />}
        </div>
      </main>
    </div>
  );
}

function ControlTab() {
  return (
    <div className="space-y-6">
      <div className="rounded-xl border border-white/5 bg-white/[0.02] p-6">
        <h3 className="text-lg font-medium mb-2">Ejecutar Pipeline</h3>
        <p className="text-sm text-gray-400 mb-4">
          Genera contenido, produce videos y publica en redes sociales usando el
          brief configurado.
        </p>
        <div className="flex items-center gap-3">
          <button
            disabled
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-pink-500/20 text-pink-400 text-sm font-medium opacity-50 cursor-not-allowed"
          >
            <Terminal className="w-4 h-4" />
            Ejecutar pipeline — disponible en Fase 2
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="rounded-xl border border-white/5 bg-white/[0.02] p-4">
          <h4 className="text-sm font-medium text-gray-400 mb-2">
            Estado de APIs
          </h4>
          <div className="space-y-2 text-sm">
            <div className="flex items-center justify-between">
              <span className="text-gray-400">Buffer</span>
              <span className="text-eko-green text-xs">Conectado</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-400">ElevenLabs TTS</span>
              <span className="text-eko-green text-xs">Activo</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-400">Hugging Face FLUX</span>
              <span className="text-eko-green text-xs">Activo</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-400">MiniMax Hailuo</span>
              <span className="text-red-400 text-xs">Agotado (reset mañana)</span>
            </div>
          </div>
        </div>

        <div className="rounded-xl border border-white/5 bg-white/[0.02] p-4">
          <h4 className="text-sm font-medium text-gray-400 mb-2">
            Límites del plan
          </h4>
          <div className="space-y-2 text-sm">
            <div className="flex items-center justify-between">
              <span className="text-gray-400">Buffer posts</span>
              <span className="text-gray-300">10 scheduled</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-400">Hailuo videos/día</span>
              <span className="text-gray-300">2/2 usados</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-400">ElevenLabs créditos</span>
              <span className="text-gray-300">~160k</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function PostsTab() {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium text-gray-400">Posts en Buffer</h3>
        <span className="text-xs text-gray-500">Gestiona publicaciones en todas las plataformas</span>
      </div>
      <PostsList />
    </div>
  );
}

function MonitorTab() {
  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-sm font-medium text-gray-400 mb-3">
          Estado de canales (Buffer)
        </h3>
        <BufferStatus />
      </div>

      <div>
        <h3 className="text-sm font-medium text-gray-400 mb-3">
          Historial de pipelines
        </h3>
        <PipelineHistory />
      </div>
    </div>
  );
}
