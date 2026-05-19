"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import {
  LayoutTemplate,
  Plus,
  Eye,
  Trash2,
  Copy,
  Star,
  RotateCcw,
  Wand2,
  Save,
  X,
  Smartphone,
  Monitor,
  Loader2,
  BarChart3,
  ExternalLink,
  TrendingUp,
  Zap,
  Flame,
  HeartPulse,
  Dumbbell,
  Droplets,
  Trophy,
  Medal,
  Layers,
} from "lucide-react";
import { landingPagesApi } from "@/lib/api";
import Link from "next/link";
import Navbar from "@/components/Navbar";
import { useT } from "@/contexts/I18nProvider";

interface LandingPage {
  id: number;
  name: string;
  slug: string;
  prompt: string | null;
  html_content: string;
  css_content: string | null;
  js_content: string | null;
  is_active: boolean;
  is_random_pool: boolean;
  analytics: {
    total_visits: number;
    unique_visits: number;
    form_fills: number;
    email_replies: number;
    calls_made: number;
    bookings_created: number;
    deals_closed: number;
    conversion_rate?: number;
  };
  created_at: string;
}

interface CompareItem {
  id: number;
  name: string;
  slug: string;
  is_active: boolean;
  is_random_pool: boolean;
  analytics: {
    total_visits: number;
    unique_visits: number;
    form_fills: number;
    conversion_rate: number;
    bookings_created: number;
    deals_closed: number;
  };
  created_at: string;
}

const PROMPT_TEMPLATES = [
  {
    id: "restaurant",
    label: "Restaurante",
    icon: Flame,
    color: "text-orange-400 bg-orange-400/10 border-orange-400/20 hover:bg-orange-400/20",
    text: "Crea una landing page para un restaurante local que resalte el menú, reservas online, y promociones de happy hour. Ton cálido y acogedor.",
  },
  {
    id: "clinic",
    label: "Clínica/Dental",
    icon: HeartPulse,
    color: "text-rose-400 bg-rose-400/10 border-rose-400/20 hover:bg-rose-400/20",
    text: "Crea una landing page para una clínica dental que enfatice servicios de emergencia, seguros aceptados, y citas online. Ton profesional y tranquilizador.",
  },
  {
    id: "gym",
    label: "Gym/Fitness",
    icon: Dumbbell,
    color: "text-emerald-400 bg-emerald-400/10 border-emerald-400/20 hover:bg-emerald-400/20",
    text: "Crea una landing page para un gimnasio local que destaque clases grupales, entrenadores personales, y membresías. Ton energético y motivador.",
  },
  {
    id: "spa",
    label: "Spa/Salón",
    icon: Droplets,
    color: "text-cyan-400 bg-cyan-400/10 border-cyan-400/20 hover:bg-cyan-400/20",
    text: "Crea una landing page para un spa que resalte masajes, tratamientos faciales, y gift cards. Ton relajante y lujoso.",
  },
];

// Normalize any API error shape to a string so it never crashes the React tree.
// FastAPI 422 returns `detail` as an array of validation objects; rendering an
// object directly as a JSX child throws "Objects are not valid as a React child".
function formatApiError(err: any, fallback: string): string {
  const detail = err?.response?.data?.detail;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((d: any) => {
        if (typeof d === "string") return d;
        const field = Array.isArray(d?.loc)
          ? d.loc.filter((x: any) => x !== "body").join(".")
          : "";
        const msg = d?.msg || JSON.stringify(d);
        return field ? `${field}: ${msg}` : msg;
      })
      .join(" · ");
  }
  if (detail && typeof detail === "object") return detail.msg || JSON.stringify(detail);
  if (err?.message) return err.message;
  return fallback;
}

// Active landing page thumbnail — scales the iframe to fill the card width
// at a fixed 16:10 aspect ratio. Recomputes scale via ResizeObserver so the
// preview always fills the available space without leaving a white frame.
function ActivePreview({ slug }: { slug: string }) {
  const ref = useRef<HTMLDivElement>(null);
  const [scale, setScale] = useState(0.25);
  const VW = 1280;
  const VH = 800;
  // Iframe is rendered wider than the visible area so the native browser
  // scrollbar (page content is taller than VH) falls past the container's
  // right edge and gets clipped by overflow-hidden. Without this buffer
  // the scrollbar shows as a white sliver on the right of the preview.
  const SCROLLBAR_BUFFER = 24;

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const update = () => setScale(el.clientWidth / VW);
    update();
    const ro = new ResizeObserver(update);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  return (
    <div
      ref={ref}
      className="relative w-full rounded-lg overflow-hidden bg-[#0F172A] mb-3 border border-[#334155]"
      style={{ aspectRatio: `${VW} / ${VH}` }}
    >
      <iframe
        src={`/api/v1/landing-pages/public/${slug}`}
        className="absolute top-0 left-0 border-0 pointer-events-none"
        style={{
          width: `${VW + SCROLLBAR_BUFFER}px`,
          height: `${VH}px`,
          transform: `scale(${scale})`,
          transformOrigin: "top left",
          colorScheme: "dark",
        }}
        sandbox="allow-scripts"
        title="Active preview"
        loading="lazy"
      />
    </div>
  );
}

export default function LandingPagesPage() {
  const [pages, setPages] = useState<LandingPage[]>([]);
  const { t } = useT();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedPage, setSelectedPage] = useState<LandingPage | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [previewMode, setPreviewMode] = useState<"desktop" | "mobile">("desktop");
  const [leftTab, setLeftTab] = useState<"pages" | "compare">("pages");
  const [compareData, setCompareData] = useState<CompareItem[]>([]);
  const [loadingCompare, setLoadingCompare] = useState(false);

  // Form state
  const [formName, setFormName] = useState("");
  const [formSlug, setFormSlug] = useState("");
  const [formPrompt, setFormPrompt] = useState("");
  const [formHtml, setFormHtml] = useState("");
  const [formTemplateId, setFormTemplateId] = useState<string>("eko-classic");

  // Available templates (loaded once on mount)
  const [templates, setTemplates] = useState<
    { id: string; name: string; tagline: string; vibe: string; best_for: string; accent: string }[]
  >([]);
  useEffect(() => {
    fetch("/content-api/lp-templates")
      .then((r) => r.json())
      .then((d) => setTemplates(d.templates || []))
      .catch(() => {});
  }, []);

  const loadPages = useCallback(async () => {
    setLoading(true);
    try {
      const res = await landingPagesApi.list();
      setPages(res.data.items || []);
      setError("");
    } catch (e: any) {
      setError(formatApiError(e, "Failed to load landing pages"));
    } finally {
      setLoading(false);
    }
  }, []);

  const loadCompare = useCallback(async () => {
    setLoadingCompare(true);
    try {
      const res = await landingPagesApi.compare();
      setCompareData(res.data || []);
    } catch (e: any) {
      setError(formatApiError(e, "Failed to load comparison"));
    } finally {
      setLoadingCompare(false);
    }
  }, []);

  useEffect(() => {
    loadPages();
    loadCompare();
  }, [loadPages, loadCompare]);

  const handleCreate = () => {
    setIsCreating(true);
    setSelectedPage(null);
    setFormName("");
    setFormSlug("");
    setFormPrompt("");
    setFormHtml("");
    setLeftTab("pages");
  };

  const handleEdit = (page: LandingPage) => {
    setIsCreating(false);
    setSelectedPage(page);
    setFormName(page.name);
    setFormSlug(page.slug);
    setFormPrompt(page.prompt || "");
    setFormHtml(page.html_content);
  };

  const handleSave = async (activate = false) => {
    try {
      if (selectedPage) {
        await landingPagesApi.update(selectedPage.id, {
          name: formName,
          slug: formSlug,
          prompt: formPrompt,
          html_content: formHtml,
        });
        if (activate) {
          await landingPagesApi.activate(selectedPage.id);
        }
      } else {
        const res = await landingPagesApi.create({
          name: formName,
          slug: formSlug,
          prompt: formPrompt,
          html_content: formHtml || "<html><body><h1>New Landing Page</h1></body></html>",
          is_active: activate,
          template_id: formTemplateId,
        } as any);
        if (activate && res.data.id) {
          await landingPagesApi.activate(res.data.id);
        }
      }
      await loadPages();
      await loadCompare();
      setIsCreating(false);
      setSelectedPage(null);
    } catch (e: any) {
      setError(formatApiError(e, "Failed to save"));
    }
  };

  const handleGenerate = async () => {
    let targetId: number | undefined = selectedPage?.id;

    // If creating, save draft first
    if (!targetId) {
      if (!formName.trim() || !formSlug.trim()) {
        setError(t("landing.error.name_slug_required"));
        return;
      }
      try {
        const res = await landingPagesApi.create({
          name: formName,
          slug: formSlug,
          prompt: formPrompt,
          html_content: formHtml || "<html><body><h1>New Landing Page</h1></body></html>",
          is_active: false,
          template_id: formTemplateId,
        } as any);
        targetId = res.data.id;
        setSelectedPage(res.data);
        setIsCreating(false);
        setError("");
        await loadPages();
        await loadCompare();
      } catch (e: any) {
        setError(formatApiError(e, "Failed to create draft"));
        return;
      }
    }

    if (!targetId) {
      setError(t("landing.error.no_id"));
      return;
    }

    setIsGenerating(true);
    try {
      await landingPagesApi.generate(targetId, { prompt: formPrompt, template_id: formTemplateId } as any);
      const res = await landingPagesApi.get(targetId);
      setSelectedPage(res.data);
      setFormHtml(res.data.html_content);
      setError("");
      await loadPages();
      await loadCompare();
    } catch (e: any) {
      const status = e.response?.status;
      const detail = e.response?.data?.detail;
      const message = detail || e.message || "Unknown error";
      setError(`${t("landing.error.generation_failed")}${status ? ` (${status})` : ""}: ${message}`);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm(t("landing.confirm.delete"))) return;
    try {
      await landingPagesApi.delete(id);
      await loadPages();
      await loadCompare();
      if (selectedPage?.id === id) {
        setSelectedPage(null);
        setIsCreating(false);
      }
    } catch (e: any) {
      setError(formatApiError(e, "Delete failed"));
    }
  };

  const handleClone = async (id: number) => {
    try {
      await landingPagesApi.clone(id);
      await loadPages();
      await loadCompare();
    } catch (e: any) {
      setError(formatApiError(e, "Clone failed"));
    }
  };

  const handleActivate = async (id: number) => {
    try {
      await landingPagesApi.activate(id);
      await loadPages();
      await loadCompare();
    } catch (e: any) {
      setError(formatApiError(e, "Activate failed"));
    }
  };

  const handleDeactivate = async (id: number) => {
    try {
      await landingPagesApi.update(id, { is_active: false });
      await loadPages();
      await loadCompare();
    } catch (e: any) {
      setError(formatApiError(e, "Deactivate failed"));
    }
  };

  const autoSlug = (name: string) => {
    return name
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "");
  };

  const activePage = pages.find((p) => p.is_active);

  const sortedCompare = [...compareData].sort((a, b) => {
    const rateA = a.analytics?.conversion_rate || 0;
    const rateB = b.analytics?.conversion_rate || 0;
    return rateB - rateA;
  });

  return (
    <div className="min-h-screen bg-[#0F172A] text-white">
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pt-20">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold flex items-center gap-3">
              <LayoutTemplate className="w-8 h-8 text-[#0B4FD8]" />
              {t("landing.title")}
            </h1>
            <p className="text-[#64748B] mt-1">
              {t("landing.subtitle")}
            </p>
          </div>
          <button
            onClick={handleCreate}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-[#0B4FD8] text-white font-medium hover:bg-[#0A3FB8] transition-colors"
          >
            <Plus className="w-4 h-4" />
            {t("landing.new_button")}
          </button>
        </div>

        {error && (
          <div className="mb-4 bg-red-500/10 border border-red-500/20 rounded-xl p-3 text-red-400 text-sm">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left panel — List / Compare */}
          <div className="lg:col-span-1 space-y-4">
            {/* Active Landing Page Card */}
            {activePage ? (
              <div className="bg-gradient-to-br from-[#0B4FD8]/20 to-[#1E293B] rounded-xl border border-[#0B4FD8]/30 overflow-hidden">
                <div className="px-4 py-2.5 border-b border-[#0B4FD8]/20 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="relative flex h-2.5 w-2.5">
                      <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                      <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
                    </span>
                    <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wider">
                      {t("landing.active.in_use")}
                    </span>
                  </div>
                  <span className="px-1.5 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-400 font-medium">
                    {t("landing.active.badge")}
                  </span>
                </div>
                <div className="p-4">
                  {/* Thumbnail — dynamic scale fills card width, dark bg */}
                  <ActivePreview slug={activePage.slug} />
                  <h3 className="font-semibold text-sm text-white mb-0.5">{activePage.name}</h3>
                  <p className="text-xs text-[#64748B] mb-2">/{activePage.slug}</p>
                  <div className="flex items-center gap-3 text-xs text-[#94A3B8] mb-3">
                    <span className="flex items-center gap-1">
                      <TrendingUp className="w-3 h-3" />
                      {activePage.analytics?.total_visits || 0} {t("landing.metric.visits")}
                    </span>
                    <span className="flex items-center gap-1">
                      <Zap className="w-3 h-3" />
                      {activePage.analytics?.conversion_rate?.toFixed?.(1) ||
                        (
                          ((activePage.analytics?.form_fills || 0) /
                            Math.max(activePage.analytics?.unique_visits || 1, 1)) *
                          100
                        ).toFixed(1)}
                      % {t("landing.metric.conv")}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <a
                      href={`/landing?lp=${activePage.slug}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-[#0B4FD8]/20 text-[#0B4FD8] text-xs font-medium hover:bg-[#0B4FD8]/30 transition-colors"
                    >
                      <ExternalLink className="w-3 h-3" />
                      {t("landing.action.view")}
                    </a>
                    <button
                      onClick={() => handleEdit(activePage)}
                      className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-[#334155] text-white text-xs font-medium hover:bg-[#475569] transition-colors"
                    >
                      <Layers className="w-3 h-3" />
                      {t("common.edit")}
                    </button>
                    <button
                      onClick={() => handleDeactivate(activePage.id)}
                      className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-[#334155] text-[#94A3B8] text-xs font-medium hover:bg-[#475569] hover:text-white transition-colors"
                    >
                      <Star className="w-3 h-3" />
                      {t("landing.action.deactivate")}
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-gradient-to-br from-[#334155]/50 to-[#1E293B] rounded-xl border border-[#334155] overflow-hidden">
                <div className="px-4 py-2.5 border-b border-[#334155] flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="relative flex h-2.5 w-2.5">
                      <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#0B4FD8] opacity-75"></span>
                      <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-[#0B4FD8]"></span>
                    </span>
                    <span className="text-xs font-semibold text-[#0B4FD8] uppercase tracking-wider">
                      {t("landing.active.in_use")}
                    </span>
                  </div>
                  <span className="px-1.5 py-0.5 rounded text-[10px] bg-[#0B4FD8]/20 text-[#0B4FD8] font-medium">
                    {t("landing.active.system")}
                  </span>
                </div>
                <div className="p-4">
                  {/* Thumbnail */}
                  <div className="relative w-full h-24 rounded-lg overflow-hidden bg-gradient-to-br from-[#0B4FD8]/10 to-[#1E293B] mb-3 border border-[#334155] flex items-center justify-center">
                    <LayoutTemplate className="w-10 h-10 text-[#0B4FD8]/30" />
                  </div>
                  <h3 className="font-semibold text-sm text-white mb-0.5">{t("landing.default.title")}</h3>
                  <p className="text-xs text-[#64748B] mb-2">/landing</p>
                  <p className="text-xs text-[#64748B] mb-3">
                    {t("landing.default.description")}
                  </p>
                  <div className="flex items-center gap-2">
                    <a
                      href="/landing"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-[#0B4FD8]/20 text-[#0B4FD8] text-xs font-medium hover:bg-[#0B4FD8]/30 transition-colors"
                    >
                      <ExternalLink className="w-3 h-3" />
                      {t("landing.action.view")}
                    </a>
                    <button
                      onClick={handleCreate}
                      className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-[#0B4FD8] text-white text-xs font-medium hover:bg-[#0A3FB8] transition-colors"
                    >
                      <Plus className="w-3 h-3" />
                      {t("landing.action.create_custom")}
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Tabs */}
            <div className="flex items-center gap-1 bg-[#1E293B] rounded-xl border border-[#334155] p-1">
              <button
                onClick={() => setLeftTab("pages")}
                className={`flex-1 flex items-center justify-center gap-1.5 py-2 rounded-lg text-xs font-medium transition-colors ${
                  leftTab === "pages"
                    ? "bg-[#334155] text-white"
                    : "text-[#64748B] hover:text-white"
                }`}
              >
                <LayoutTemplate className="w-3.5 h-3.5" />
                {t("landing.tab.pages")} ({pages.length})
              </button>
              <button
                onClick={() => setLeftTab("compare")}
                className={`flex-1 flex items-center justify-center gap-1.5 py-2 rounded-lg text-xs font-medium transition-colors ${
                  leftTab === "compare"
                    ? "bg-[#334155] text-white"
                    : "text-[#64748B] hover:text-white"
                }`}
              >
                <BarChart3 className="w-3.5 h-3.5" />
                {t("landing.tab.compare")}
              </button>
            </div>

            {leftTab === "pages" ? (
              <div className="bg-[#1E293B] rounded-xl border border-[#334155] overflow-hidden">
                <div className="px-4 py-3 border-b border-[#334155] flex items-center justify-between">
                  <span className="text-sm font-medium text-[#94A3B8]">
                    {pages.length} {pages.length !== 1 ? t("landing.list.pages_plural") : t("landing.list.pages_singular")}
                  </span>
                </div>
                <div className="divide-y divide-[#334155]">
                  {loading ? (
                    <div className="p-8 text-center text-[#64748B]">
                      <Loader2 className="w-6 h-6 animate-spin mx-auto mb-2" />
                      {t("common.loading")}
                    </div>
                  ) : pages.length === 0 ? (
                    <div className="p-8 text-center text-[#64748B]">
                      {t("landing.list.empty")}
                    </div>
                  ) : (
                    pages.map((page) => (
                      <div
                        key={page.id}
                        onClick={() => handleEdit(page)}
                        className={`px-4 py-3 cursor-pointer hover:bg-[#334155]/30 transition-colors ${
                          selectedPage?.id === page.id ? "bg-[#334155]/50" : ""
                        }`}
                      >
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-medium text-sm truncate">{page.name}</span>
                          <div className="flex items-center gap-1">
                            {page.is_active && (
                              <span className="px-1.5 py-0.5 rounded text-[10px] bg-[#0B4FD8]/20 text-[#0B4FD8] font-medium">
                                {t("landing.badge.active")}
                              </span>
                            )}
                            {page.is_random_pool && (
                              <span className="px-1.5 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-400 font-medium">
                                {t("landing.badge.pool")}
                              </span>
                            )}
                          </div>
                        </div>
                        <div className="flex items-center justify-between text-xs text-[#64748B]">
                          <span>/{page.slug}</span>
                          <span>{page.analytics?.total_visits || 0} {t("landing.metric.visits")}</span>
                        </div>
                        <div className="flex items-center gap-1 mt-2">
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              window.open(`/api/v1/landing-pages/public/${page.slug}`, "_blank");
                            }}
                            className="p-1 rounded hover:bg-[#334155] text-[#64748B] hover:text-white transition-colors"
                            title={t("landing.action.preview")}
                          >
                            <Eye className="w-3.5 h-3.5" />
                          </button>
                          {page.is_active ? (
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                handleDeactivate(page.id);
                              }}
                              className="px-2 py-1 rounded text-[10px] font-medium bg-emerald-500/20 text-emerald-400 hover:bg-emerald-500/30 transition-colors"
                              title={t("landing.action.deactivate")}
                            >
                              {t("landing.action.deactivate")}
                            </button>
                          ) : (
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                handleActivate(page.id);
                              }}
                              className="px-2 py-1 rounded text-[10px] font-medium bg-[#0B4FD8]/20 text-[#0B4FD8] hover:bg-[#0B4FD8]/30 transition-colors"
                              title={t("landing.action.activate")}
                            >
                              {t("landing.action.activate")}
                            </button>
                          )}
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleClone(page.id);
                            }}
                            className="p-1 rounded hover:bg-[#334155] text-[#64748B] hover:text-white transition-colors"
                            title={t("landing.action.clone")}
                          >
                            <Copy className="w-3.5 h-3.5" />
                          </button>
                          <Link
                            href={`/landing-pages/${page.id}/analytics`}
                            onClick={(e) => e.stopPropagation()}
                            className="p-1 rounded hover:bg-[#334155] text-[#64748B] hover:text-white transition-colors"
                            title={t("landing.action.analytics")}
                          >
                            <BarChart3 className="w-3.5 h-3.5" />
                          </Link>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleDelete(page.id);
                            }}
                            className="p-1 rounded hover:bg-[#334155] text-[#64748B] hover:text-red-400 transition-colors"
                            title={t("common.delete")}
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            ) : (
              <div className="bg-[#1E293B] rounded-xl border border-[#334155] overflow-hidden">
                <div className="px-4 py-3 border-b border-[#334155]">
                  <span className="text-sm font-medium text-[#94A3B8]">{t("landing.compare.title")}</span>
                </div>
                <div className="p-4">
                  {loadingCompare ? (
                    <div className="text-center text-[#64748B]">
                      <Loader2 className="w-5 h-5 animate-spin mx-auto mb-2" />
                      {t("common.loading")}
                    </div>
                  ) : compareData.length === 0 ? (
                    <p className="text-sm text-[#64748B] text-center">
                      {t("landing.compare.empty")}
                    </p>
                  ) : (
                    <div className="space-y-3">
                      {sortedCompare.map((item, idx) => (
                        <div
                          key={item.id}
                          className={`p-3 rounded-lg border ${
                            item.is_active
                              ? "border-[#0B4FD8]/30 bg-[#0B4FD8]/5"
                              : "border-[#334155] bg-[#0F172A]"
                          }`}
                        >
                          <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center gap-2">
                              {idx === 0 && compareData.length > 1 && (
                                <Trophy className="w-4 h-4 text-yellow-400" />
                              )}
                              {idx === 1 && compareData.length > 2 && (
                                <Medal className="w-4 h-4 text-gray-400" />
                              )}
                              {idx === 2 && compareData.length > 3 && (
                                <Medal className="w-4 h-4 text-amber-600" />
                              )}
                              <span className="text-sm font-medium">{item.name}</span>
                            </div>
                            {item.is_active && (
                              <span className="px-1.5 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-400 font-medium">
                                {t("landing.badge.active")}
                              </span>
                            )}
                          </div>
                          <div className="grid grid-cols-3 gap-2 text-xs">
                            <div>
                              <span className="text-[#64748B] block">{t("landing.compare.visits")}</span>
                              <span className="text-white font-medium">
                                {item.analytics?.total_visits?.toLocaleString?.() || 0}
                              </span>
                            </div>
                            <div>
                              <span className="text-[#64748B] block">{t("landing.compare.forms")}</span>
                              <span className="text-white font-medium">
                                {item.analytics?.form_fills || 0}
                              </span>
                            </div>
                            <div>
                              <span className="text-[#64748B] block">{t("landing.compare.conv")}</span>
                              <span
                                className={`font-medium ${
                                  (item.analytics?.conversion_rate || 0) > 5
                                    ? "text-emerald-400"
                                    : "text-white"
                                }`}
                              >
                                {item.analytics?.conversion_rate?.toFixed?.(1) || 0}%
                              </span>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Right panel — Editor / Preview */}
          <div className="lg:col-span-2">
            {isCreating || selectedPage ? (
              <div className="bg-[#1E293B] rounded-xl border border-[#334155] overflow-hidden">
                {/* Editor header */}
                <div className="px-4 py-3 border-b border-[#334155] flex items-center justify-between">
                  <span className="font-medium text-sm">
                    {isCreating ? t("landing.editor.create_title") : `${t("landing.editor.edit_prefix")}: ${selectedPage?.name}`}
                  </span>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => {
                        setIsCreating(false);
                        setSelectedPage(null);
                      }}
                      className="p-1.5 rounded hover:bg-[#334155] text-[#64748B] transition-colors"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                <div className="p-4 space-y-4">
                  {/* Name & Slug */}
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-xs font-medium text-[#64748B] mb-1">{t("landing.field.name")}</label>
                      <input
                        type="text"
                        value={formName}
                        onChange={(e) => {
                          setFormName(e.target.value);
                          if (isCreating) setFormSlug(autoSlug(e.target.value));
                        }}
                        className="w-full bg-[#0F172A] border border-[#334155] rounded-lg px-3 py-2 text-sm text-white placeholder-[#64748B] focus:outline-none focus:border-[#0B4FD8]"
                        placeholder={t("landing.field.name_placeholder")}
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-medium text-[#64748B] mb-1">{t("landing.field.slug")}</label>
                      <input
                        type="text"
                        value={formSlug}
                        onChange={(e) => setFormSlug(e.target.value)}
                        className="w-full bg-[#0F172A] border border-[#334155] rounded-lg px-3 py-2 text-sm text-white placeholder-[#64748B] focus:outline-none focus:border-[#0B4FD8]"
                        placeholder={t("landing.field.slug_placeholder")}
                      />
                    </div>
                  </div>

                  {/* Template selector — grid of 10 design templates */}
                  {isCreating && templates.length > 0 && (
                    <div>
                      <label className="block text-xs font-medium text-[#64748B] mb-2">
                        {t("landing.template.choose")} ({templates.length} {t("landing.template.designs")})
                      </label>
                      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2.5">
                        {templates.map((tpl) => {
                          const isSelected = formTemplateId === tpl.id;
                          return (
                            <button
                              key={tpl.id}
                              type="button"
                              onClick={() => setFormTemplateId(tpl.id)}
                              className={`relative text-left p-0 rounded-lg overflow-hidden border-2 transition-all ${
                                isSelected
                                  ? "border-[#0B4FD8] shadow-lg shadow-[#0B4FD8]/30"
                                  : "border-[#334155] hover:border-[#475569]"
                              }`}
                              style={{ background: "#0F172A" }}
                              title={`${tpl.name} — ${tpl.tagline}\nBest for: ${tpl.best_for}`}
                            >
                              {/* Thumbnail iframe — preview of the template with sample copy */}
                              <div
                                className="relative w-full overflow-hidden"
                                style={{ aspectRatio: "16 / 10", background: tpl.accent + "10" }}
                              >
                                <iframe
                                  src={`/api/v1/landing-pages/template-preview/${tpl.id}`}
                                  className="absolute top-0 left-0 border-0 pointer-events-none"
                                  style={{
                                    width: "1304px",
                                    height: "800px",
                                    transform: "scale(0.15)",
                                    transformOrigin: "top left",
                                    colorScheme: "dark",
                                  }}
                                  sandbox="allow-scripts"
                                  title={`${tpl.name} preview`}
                                  loading="lazy"
                                />
                                {isSelected && (
                                  <div className="absolute top-1.5 right-1.5 bg-[#0B4FD8] text-white rounded-full w-5 h-5 flex items-center justify-center text-[10px] font-bold shadow-md">
                                    ✓
                                  </div>
                                )}
                              </div>
                              {/* Name + accent bar */}
                              <div className="px-2 py-1.5 border-t border-[#334155]">
                                <div className="flex items-center gap-1.5">
                                  <span
                                    className="block w-2 h-2 rounded-full flex-shrink-0"
                                    style={{ background: tpl.accent }}
                                  />
                                  <span className="text-[11px] font-semibold text-white truncate">
                                    {tpl.name}
                                  </span>
                                </div>
                                <span className="block text-[10px] text-[#64748B] truncate mt-0.5">
                                  {tpl.best_for}
                                </span>
                              </div>
                            </button>
                          );
                        })}
                      </div>
                    </div>
                  )}

                  {/* Prompt */}
                  <div>
                    <label className="block text-xs font-medium text-[#64748B] mb-1">
                      {t("landing.field.ai_prompt")} {isCreating && <span className="text-[#64748B]">{t("landing.field.ai_prompt_hint")}</span>}
                    </label>
                    <textarea
                      value={formPrompt}
                      onChange={(e) => setFormPrompt(e.target.value)}
                      rows={3}
                      className="w-full bg-[#0F172A] border border-[#334155] rounded-lg px-3 py-2 text-sm text-white placeholder-[#64748B] focus:outline-none focus:border-[#0B4FD8] resize-none"
                      placeholder={t("landing.field.ai_prompt_placeholder")}
                    />
                    {/* Template chips */}
                    <div className="flex flex-wrap gap-2 mt-2">
                      {PROMPT_TEMPLATES.map((tmpl) => (
                        <button
                          key={tmpl.id}
                          onClick={() => setFormPrompt(tmpl.text)}
                          className={`inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-medium border transition-colors ${tmpl.color}`}
                        >
                          <tmpl.icon className="w-3.5 h-3.5" />
                          {tmpl.label}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Action buttons */}
                  <div className="flex items-center gap-2 flex-wrap">
                    {/* Primary: Generate with AI */}
                    <button
                      onClick={handleGenerate}
                      disabled={isGenerating || !formPrompt.trim()}
                      className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-gradient-to-r from-[#0B4FD8] to-[#22D3EE] text-white text-sm font-semibold hover:from-[#0A3FB8] hover:to-[#1CB8D0] transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-[#0B4FD8]/20"
                      title={!formPrompt.trim() ? t("landing.action.add_prompt_first") : ""}
                    >
                      {isGenerating ? (
                        <Loader2 className="w-4 h-4 animate-spin" />
                      ) : (
                        <Wand2 className="w-4 h-4" />
                      )}
                      {isGenerating ? t("landing.action.generating") : t("landing.action.generate_ai")}
                    </button>

                    <div className="w-px h-6 bg-[#334155] mx-1" />

                    <button
                      onClick={() => handleSave(false)}
                      disabled={!formName.trim() || !formSlug.trim()}
                      title={!formName.trim() || !formSlug.trim() ? t("landing.action.name_slug_required_tooltip") : ""}
                      className="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg bg-[#334155] text-white text-sm font-medium hover:bg-[#475569] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <Save className="w-3.5 h-3.5" />
                      {t("landing.action.save_draft")}
                    </button>
                    <button
                      onClick={() => handleSave(true)}
                      disabled={!formName.trim() || !formSlug.trim()}
                      title={!formName.trim() || !formSlug.trim() ? t("landing.action.name_slug_required_tooltip") : ""}
                      className="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg bg-[#0B4FD8] text-white text-sm font-medium hover:bg-[#0A3FB8] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <Star className="w-3.5 h-3.5" />
                      {t("landing.action.save_activate")}
                    </button>
                    <button
                      onClick={() => {
                        if (selectedPage) {
                          setFormHtml(selectedPage.html_content);
                          setFormPrompt(selectedPage.prompt || "");
                          setFormName(selectedPage.name);
                          setFormSlug(selectedPage.slug);
                        } else {
                          setFormName("");
                          setFormSlug("");
                          setFormPrompt("");
                          setFormHtml("");
                        }
                      }}
                      className="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg bg-[#334155] text-white text-sm font-medium hover:bg-[#475569] transition-colors"
                    >
                      <RotateCcw className="w-3.5 h-3.5" />
                      {t("common.reset")}
                    </button>
                  </div>

                  {/* HTML Editor */}
                  <div>
                    <label className="block text-xs font-medium text-[#64748B] mb-1">{t("landing.field.html")}</label>
                    <textarea
                      value={formHtml}
                      onChange={(e) => setFormHtml(e.target.value)}
                      rows={8}
                      className="w-full bg-[#0F172A] border border-[#334155] rounded-lg px-3 py-2 text-xs text-white font-mono placeholder-[#64748B] focus:outline-none focus:border-[#0B4FD8] resize-none"
                      placeholder="<html>...</html>"
                    />
                  </div>

                  {/* Active Toggle */}
                  {selectedPage && (
                    <div className="flex items-center justify-between py-2 px-3 bg-[#0F172A] rounded-lg border border-[#334155]">
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-medium text-white">{t("landing.toggle.main_label")}</span>
                        <span className="text-xs text-[#64748B]">
                          {selectedPage.is_active ? t("landing.toggle.active_hint") : t("landing.toggle.inactive_hint")}
                        </span>
                      </div>
                      <button
                        onClick={async () => {
                          if (!selectedPage) return;
                          try {
                            if (selectedPage.is_active) {
                              await landingPagesApi.update(selectedPage.id, { is_active: false });
                            } else {
                              await landingPagesApi.activate(selectedPage.id);
                            }
                            const res = await landingPagesApi.get(selectedPage.id);
                            setSelectedPage(res.data);
                            await loadPages();
                            await loadCompare();
                          } catch (e: any) {
                            setError(formatApiError(e, "Failed to toggle active state"));
                          }
                        }}
                        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                          selectedPage.is_active ? "bg-[#0B4FD8]" : "bg-[#334155]"
                        }`}
                      >
                        <span
                          className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                            selectedPage.is_active ? "translate-x-6" : "translate-x-1"
                          }`}
                        />
                      </button>
                    </div>
                  )}

                  {/* Preview */}
                  {formHtml && (
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <label className="text-xs font-medium text-[#64748B]">{t("landing.preview.label")}</label>
                        <div className="flex items-center gap-1 bg-[#0F172A] rounded-lg p-0.5">
                          <button
                            onClick={() => setPreviewMode("desktop")}
                            className={`p-1 rounded transition-colors ${
                              previewMode === "desktop" ? "bg-[#334155] text-white" : "text-[#64748B]"
                            }`}
                          >
                            <Monitor className="w-3.5 h-3.5" />
                          </button>
                          <button
                            onClick={() => setPreviewMode("mobile")}
                            className={`p-1 rounded transition-colors ${
                              previewMode === "mobile" ? "bg-[#334155] text-white" : "text-[#64748B]"
                            }`}
                          >
                            <Smartphone className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      </div>
                      <div
                        className={`border border-[#334155] rounded-lg ${
                          previewMode === "mobile" ? "max-w-[375px] mx-auto" : "w-full"
                        }`}
                        style={{
                          height: "500px",
                          overflow: "auto",
                          backgroundImage: "radial-gradient(circle, #334155 1px, transparent 1px)",
                          backgroundSize: "20px 20px",
                        }}
                      >
                        <iframe
                          srcDoc={formHtml}
                          className="w-full h-full"
                          sandbox="allow-scripts"
                          title="Preview"
                          style={{ background: "transparent" }}
                        />
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="bg-[#1E293B] rounded-xl border border-[#334155] p-12 text-center">
                <LayoutTemplate className="w-12 h-12 text-[#64748B] mx-auto mb-4" />
                <h3 className="text-lg font-medium text-white mb-2">{t("landing.empty.title")}</h3>
                <p className="text-[#64748B] mb-4">
                  {t("landing.empty.description")}
                </p>
                <button
                  onClick={handleCreate}
                  className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-[#0B4FD8] text-white font-medium hover:bg-[#0A3FB8] transition-colors"
                >
                  <Plus className="w-4 h-4" />
                  {t("landing.action.create_new")}
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
