"use client";

import { useState, useEffect, useCallback } from "react";
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
} from "lucide-react";
import { landingPagesApi } from "@/lib/api";
import Link from "next/link";

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
  };
  created_at: string;
}

export default function LandingPagesPage() {
  const [pages, setPages] = useState<LandingPage[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedPage, setSelectedPage] = useState<LandingPage | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [previewMode, setPreviewMode] = useState<"desktop" | "mobile">("desktop");

  // Form state
  const [formName, setFormName] = useState("");
  const [formSlug, setFormSlug] = useState("");
  const [formPrompt, setFormPrompt] = useState("");
  const [formHtml, setFormHtml] = useState("");

  const loadPages = useCallback(async () => {
    setLoading(true);
    try {
      const res = await landingPagesApi.list();
      setPages(res.data.items || []);
      setError("");
    } catch (e: any) {
      setError(e.response?.data?.detail || "Failed to load landing pages");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadPages();
  }, [loadPages]);

  const handleCreate = () => {
    setIsCreating(true);
    setSelectedPage(null);
    setFormName("");
    setFormSlug("");
    setFormPrompt("");
    setFormHtml("");
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
        });
        if (activate && res.data.id) {
          await landingPagesApi.activate(res.data.id);
        }
      }
      await loadPages();
      setIsCreating(false);
      setSelectedPage(null);
    } catch (e: any) {
      setError(e.response?.data?.detail || "Failed to save");
    }
  };

  const handleGenerate = async () => {
    const targetId = selectedPage?.id;
    if (!targetId) {
      setError("Save a draft first, then generate");
      return;
    }
    setIsGenerating(true);
    try {
      await landingPagesApi.generate(targetId, { prompt: formPrompt });
      const res = await landingPagesApi.get(targetId);
      setSelectedPage(res.data);
      setFormHtml(res.data.html_content);
      setError("");
    } catch (e: any) {
      setError(e.response?.data?.detail || "Generation failed");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Delete this landing page?")) return;
    try {
      await landingPagesApi.delete(id);
      await loadPages();
      if (selectedPage?.id === id) {
        setSelectedPage(null);
        setIsCreating(false);
      }
    } catch (e: any) {
      setError(e.response?.data?.detail || "Delete failed");
    }
  };

  const handleClone = async (id: number) => {
    try {
      await landingPagesApi.clone(id);
      await loadPages();
    } catch (e: any) {
      setError(e.response?.data?.detail || "Clone failed");
    }
  };

  const handleActivate = async (id: number) => {
    try {
      await landingPagesApi.activate(id);
      await loadPages();
    } catch (e: any) {
      setError(e.response?.data?.detail || "Activate failed");
    }
  };

  const autoSlug = (name: string) => {
    return name
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "");
  };

  return (
    <div className="min-h-screen bg-[#0F172A] text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold flex items-center gap-3">
              <LayoutTemplate className="w-8 h-8 text-[#0B4FD8]" />
              Landing Pages
            </h1>
            <p className="text-[#64748B] mt-1">
              Create, manage, and A/B test your landing pages with AI.
            </p>
          </div>
          <button
            onClick={handleCreate}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-[#0B4FD8] text-white font-medium hover:bg-[#0A3FB8] transition-colors"
          >
            <Plus className="w-4 h-4" />
            New Landing Page
          </button>
        </div>

        {error && (
          <div className="mb-4 bg-red-500/10 border border-red-500/20 rounded-xl p-3 text-red-400 text-sm">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left panel — List */}
          <div className="lg:col-span-1 space-y-4">
            <div className="bg-[#1E293B] rounded-xl border border-[#334155] overflow-hidden">
              <div className="px-4 py-3 border-b border-[#334155] flex items-center justify-between">
                <span className="text-sm font-medium text-[#94A3B8]">
                  {pages.length} page{pages.length !== 1 ? "s" : ""}
                </span>
              </div>
              <div className="divide-y divide-[#334155]">
                {loading ? (
                  <div className="p-8 text-center text-[#64748B]">
                    <Loader2 className="w-6 h-6 animate-spin mx-auto mb-2" />
                    Loading...
                  </div>
                ) : pages.length === 0 ? (
                  <div className="p-8 text-center text-[#64748B]">
                    No landing pages yet. Create your first one!
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
                              Active
                            </span>
                          )}
                          {page.is_random_pool && (
                            <span className="px-1.5 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-400 font-medium">
                              Pool
                            </span>
                          )}
                        </div>
                      </div>
                      <div className="flex items-center justify-between text-xs text-[#64748B]">
                        <span>/{page.slug}</span>
                        <span>{page.analytics?.total_visits || 0} visits</span>
                      </div>
                      <div className="flex items-center gap-1 mt-2">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            window.open(`/api/v1/landing-pages/public/${page.slug}`, "_blank");
                          }}
                          className="p-1 rounded hover:bg-[#334155] text-[#64748B] hover:text-white transition-colors"
                          title="Preview"
                        >
                          <Eye className="w-3.5 h-3.5" />
                        </button>
                        {!page.is_active && (
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleActivate(page.id);
                            }}
                            className="p-1 rounded hover:bg-[#334155] text-[#64748B] hover:text-yellow-400 transition-colors"
                            title="Activate"
                          >
                            <Star className="w-3.5 h-3.5" />
                          </button>
                        )}
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleClone(page.id);
                          }}
                          className="p-1 rounded hover:bg-[#334155] text-[#64748B] hover:text-white transition-colors"
                          title="Clone"
                        >
                          <Copy className="w-3.5 h-3.5" />
                        </button>
                        <Link
                          href={`/landing-pages/${page.id}/analytics`}
                          onClick={(e) => e.stopPropagation()}
                          className="p-1 rounded hover:bg-[#334155] text-[#64748B] hover:text-white transition-colors"
                          title="Analytics"
                        >
                          <BarChart3 className="w-3.5 h-3.5" />
                        </Link>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleDelete(page.id);
                          }}
                          className="p-1 rounded hover:bg-[#334155] text-[#64748B] hover:text-red-400 transition-colors"
                          title="Delete"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

          {/* Right panel — Editor / Preview */}
          <div className="lg:col-span-2">
            {(isCreating || selectedPage) ? (
              <div className="bg-[#1E293B] rounded-xl border border-[#334155] overflow-hidden">
                {/* Editor header */}
                <div className="px-4 py-3 border-b border-[#334155] flex items-center justify-between">
                  <span className="font-medium text-sm">
                    {isCreating ? "Create Landing Page" : `Edit: ${selectedPage?.name}`}
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
                      <label className="block text-xs font-medium text-[#64748B] mb-1">Name</label>
                      <input
                        type="text"
                        value={formName}
                        onChange={(e) => {
                          setFormName(e.target.value);
                          if (isCreating) setFormSlug(autoSlug(e.target.value));
                        }}
                        className="w-full bg-[#0F172A] border border-[#334155] rounded-lg px-3 py-2 text-sm text-white placeholder-[#64748B] focus:outline-none focus:border-[#0B4FD8]"
                        placeholder="My Landing Page"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-medium text-[#64748B] mb-1">Slug</label>
                      <input
                        type="text"
                        value={formSlug}
                        onChange={(e) => setFormSlug(e.target.value)}
                        className="w-full bg-[#0F172A] border border-[#334155] rounded-lg px-3 py-2 text-sm text-white placeholder-[#64748B] focus:outline-none focus:border-[#0B4FD8]"
                        placeholder="my-landing-page"
                      />
                    </div>
                  </div>

                  {/* Prompt */}
                  <div>
                    <label className="block text-xs font-medium text-[#64748B] mb-1">
                      AI Prompt
                    </label>
                    <textarea
                      value={formPrompt}
                      onChange={(e) => setFormPrompt(e.target.value)}
                      rows={3}
                      className="w-full bg-[#0F172A] border border-[#334155] rounded-lg px-3 py-2 text-sm text-white placeholder-[#64748B] focus:outline-none focus:border-[#0B4FD8] resize-none"
                      placeholder="Describe your landing page: target audience, tone, key benefits, CTA..."
                    />
                  </div>

                  {/* Action buttons */}
                  <div className="flex items-center gap-2 flex-wrap">
                    <button
                      onClick={() => handleSave(false)}
                      className="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg bg-[#334155] text-white text-sm font-medium hover:bg-[#475569] transition-colors"
                    >
                      <Save className="w-3.5 h-3.5" />
                      Save Draft
                    </button>
                    <button
                      onClick={() => handleSave(true)}
                      className="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg bg-[#0B4FD8] text-white text-sm font-medium hover:bg-[#0A3FB8] transition-colors"
                    >
                      <Star className="w-3.5 h-3.5" />
                      Save & Activate
                    </button>
                    {selectedPage && (
                      <button
                        onClick={handleGenerate}
                        disabled={isGenerating}
                        className="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg bg-emerald-600 text-white text-sm font-medium hover:bg-emerald-700 transition-colors disabled:opacity-60"
                      >
                        {isGenerating ? (
                          <Loader2 className="w-3.5 h-3.5 animate-spin" />
                        ) : (
                          <Wand2 className="w-3.5 h-3.5" />
                        )}
                        {isGenerating ? "Generating..." : "Generate with AI"}
                      </button>
                    )}
                    <button
                      onClick={() => setFormHtml(formHtml)}
                      className="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg bg-[#334155] text-white text-sm font-medium hover:bg-[#475569] transition-colors"
                    >
                      <RotateCcw className="w-3.5 h-3.5" />
                      Reset
                    </button>
                  </div>

                  {/* HTML Editor */}
                  <div>
                    <label className="block text-xs font-medium text-[#64748B] mb-1">HTML</label>
                    <textarea
                      value={formHtml}
                      onChange={(e) => setFormHtml(e.target.value)}
                      rows={8}
                      className="w-full bg-[#0F172A] border border-[#334155] rounded-lg px-3 py-2 text-xs text-white font-mono placeholder-[#64748B] focus:outline-none focus:border-[#0B4FD8] resize-none"
                      placeholder="<html>...</html>"
                    />
                  </div>

                  {/* Preview */}
                  {formHtml && (
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <label className="text-xs font-medium text-[#64748B]">Preview</label>
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
                        className={`border border-[#334155] rounded-lg overflow-hidden bg-white ${
                          previewMode === "mobile" ? "max-w-[375px] mx-auto" : "w-full"
                        }`}
                        style={{ height: "500px" }}
                      >
                        <iframe
                          srcDoc={formHtml}
                          className="w-full h-full"
                          sandbox="allow-scripts"
                          title="Preview"
                        />
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="bg-[#1E293B] rounded-xl border border-[#334155] p-12 text-center">
                <LayoutTemplate className="w-12 h-12 text-[#64748B] mx-auto mb-4" />
                <h3 className="text-lg font-medium text-white mb-2">Select or create a landing page</h3>
                <p className="text-[#64748B] mb-4">
                  Choose a landing page from the list to edit, or create a new one.
                </p>
                <button
                  onClick={handleCreate}
                  className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-[#0B4FD8] text-white font-medium hover:bg-[#0A3FB8] transition-colors"
                >
                  <Plus className="w-4 h-4" />
                  Create New
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
