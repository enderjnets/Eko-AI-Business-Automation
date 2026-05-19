"use client";

import { useState } from "react";
import { useT } from "@/contexts/I18nProvider";
import Navbar from "@/components/Navbar";
import PipelineHistory from "@/components/content-studio/PipelineHistory";
import BufferStatus from "@/components/content-studio/BufferStatus";
import PostsList from "@/components/content-studio/PostsList";
import PostCalendar from "@/components/content-studio/PostCalendar";
import AnalyticsDashboard from "@/components/content-studio/AnalyticsDashboard";
import RunPipelinePanel from "@/components/content-studio/RunPipelinePanel";
import VideosList from "@/components/content-studio/VideosList";
import {
  Play,
  Activity,
  BarChart3,
  Clapperboard,
  FileText,
  Calendar,
  Video,
} from "lucide-react";

export default function ContentStudioPage() {
  const [activeTab, setActiveTab] = useState("posts");
  const { t } = useT();

  const TABS = [
    { id: "control", label: t("content.tab.control"), icon: Play },
    { id: "videos", label: t("content.tab.videos"), icon: Video },
    { id: "posts", label: t("content.tab.posts"), icon: FileText },
    { id: "calendar", label: t("content.tab.calendar"), icon: Calendar },
    { id: "analytics", label: t("content.tab.analytics"), icon: BarChart3 },
    { id: "monitor", label: t("content.tab.monitor"), icon: Activity },
  ];

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
              {t("content.title")}
            </h1>
          </div>
          <p className="text-gray-400 text-sm">
            {t("content.subtitle")}
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
          {activeTab === "videos" && <VideosTab />}
          {activeTab === "posts" && <PostsTab />}
          {activeTab === "calendar" && <CalendarTab />}
          {activeTab === "analytics" && <AnalyticsTab />}
          {activeTab === "monitor" && <MonitorTab />}
        </div>
      </main>
    </div>
  );
}

function ControlTab() {
  return <RunPipelinePanel />;
}

function VideosTab() {
  return (
    <div className="space-y-4">
      <VideosList />
    </div>
  );
}

function PostsTab() {
  const { t } = useT();
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium text-gray-400">{t("content.posts.header")}</h3>
        <span className="text-xs text-gray-500">{t("content.posts.subheader")}</span>
      </div>
      <PostsList />
    </div>
  );
}

function CalendarTab() {
  return (
    <div className="space-y-4">
      <PostCalendar />
    </div>
  );
}

function AnalyticsTab() {
  return (
    <div className="space-y-4">
      <AnalyticsDashboard />
    </div>
  );
}

function MonitorTab() {
  const { t } = useT();
  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-sm font-medium text-gray-400 mb-3">
          {t("content.monitor.channels")}
        </h3>
        <BufferStatus />
      </div>

      <div>
        <h3 className="text-sm font-medium text-gray-400 mb-3">
          {t("content.monitor.history")}
        </h3>
        <PipelineHistory />
      </div>
    </div>
  );
}
