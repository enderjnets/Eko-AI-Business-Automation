"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import {
  ArrowLeft,
  Eye,
  Users,
  Mail,
  Phone,
  Calendar,
  Briefcase,
  TrendingUp,
  Loader2,
} from "lucide-react";
import { landingPagesApi } from "@/lib/api";
import Navbar from "@/components/Navbar";

interface AnalyticsData {
  landing_page_id: number;
  name: string;
  slug: string;
  analytics: {
    total_visits: number;
    unique_visits: number;
    form_fills: number;
    email_replies: number;
    calls_made: number;
    bookings_created: number;
    deals_closed: number;
    conversion_rate: number;
  };
  time_series: { date: string; visits: number }[];
  leads: {
    id: number;
    business_name: string;
    email: string;
    status: string;
    score: number;
    created_at: string;
  }[];
}

export default function LandingPageAnalyticsPage() {
  const params = useParams();
  const id = Number(params.id);
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!id) return;
    loadAnalytics();
  }, [id]);

  const loadAnalytics = async () => {
    setLoading(true);
    try {
      const res = await landingPagesApi.analytics(id);
      setData(res.data);
      setError("");
    } catch (e: any) {
      setError(e.response?.data?.detail || "Failed to load analytics");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0F172A] text-white flex items-center justify-center pt-16">
        <Loader2 className="w-8 h-8 animate-spin text-[#0B4FD8]" />
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-[#0F172A] text-white p-8 pt-20">
        <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-4 text-red-400">
          {error || "No data"}
        </div>
      </div>
    );
  }

  const { analytics, time_series, leads } = data;

  const kpis = [
    { label: "Total Visits", value: analytics.total_visits, icon: Eye },
    { label: "Unique Visits", value: analytics.unique_visits, icon: Users },
    { label: "Form Fills", value: analytics.form_fills, icon: Mail },
    { label: "Conversion Rate", value: `${analytics.conversion_rate}%`, icon: TrendingUp },
    { label: "Email Replies", value: analytics.email_replies, icon: Mail },
    { label: "Calls Made", value: analytics.calls_made, icon: Phone },
    { label: "Bookings", value: analytics.bookings_created, icon: Calendar },
    { label: "Deals Closed", value: analytics.deals_closed, icon: Briefcase },
  ];

  return (
    <div className="min-h-screen bg-[#0F172A] text-white pt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Link
          href="/landing-pages"
          className="inline-flex items-center gap-2 text-[#64748B] hover:text-white transition-colors mb-6"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Landing Pages
        </Link>

        <div className="mb-8">
          <h1 className="text-3xl font-bold">{data.name}</h1>
          <p className="text-[#64748B] mt-1">Analytics for /{data.slug}</p>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {kpis.map((kpi) => (
            <div
              key={kpi.label}
              className="bg-[#1E293B] rounded-xl border border-[#334155] p-4"
            >
              <div className="flex items-center gap-2 mb-2">
                <kpi.icon className="w-4 h-4 text-[#0B4FD8]" />
                <span className="text-xs text-[#64748B]">{kpi.label}</span>
              </div>
              <div className="text-2xl font-bold">{kpi.value}</div>
            </div>
          ))}
        </div>

        {/* Time Series Chart */}
        {time_series.length > 0 && (
          <div className="bg-[#1E293B] rounded-xl border border-[#334155] p-4 mb-8">
            <h3 className="text-sm font-medium mb-4">Visits (Last 30 Days)</h3>
            <div className="flex items-end gap-1 h-40">
              {time_series.map((point) => (
                <div
                  key={point.date}
                  className="flex-1 bg-[#0B4FD8] rounded-t hover:bg-[#22D3EE] transition-colors"
                  style={{
                    height: `${Math.max(
                      5,
                      (point.visits /
                        Math.max(...time_series.map((p) => p.visits))) *
                        100
                    )}%`,
                  }}
                  title={`${point.date}: ${point.visits} visits`}
                />
              ))}
            </div>
            <div className="flex justify-between text-[10px] text-[#64748B] mt-2">
              <span>{time_series[0]?.date}</span>
              <span>{time_series[time_series.length - 1]?.date}</span>
            </div>
          </div>
        )}

        {/* Leads Table */}
        <div className="bg-[#1E293B] rounded-xl border border-[#334155] overflow-hidden">
          <div className="px-4 py-3 border-b border-[#334155]">
            <h3 className="text-sm font-medium">Leads Generated</h3>
          </div>
          {leads.length === 0 ? (
            <div className="p-8 text-center text-[#64748B]">No leads yet</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-[#334155] text-[#64748B]">
                    <th className="px-4 py-2 text-left">Business</th>
                    <th className="px-4 py-2 text-left">Email</th>
                    <th className="px-4 py-2 text-left">Status</th>
                    <th className="px-4 py-2 text-left">Score</th>
                    <th className="px-4 py-2 text-left">Date</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#334155]">
                  {leads.map((lead) => (
                    <tr key={lead.id} className="hover:bg-[#334155]/20">
                      <td className="px-4 py-2">
                        <Link
                          href={`/leads/${lead.id}`}
                          className="text-[#0B4FD8] hover:underline"
                        >
                          {lead.business_name}
                        </Link>
                      </td>
                      <td className="px-4 py-2 text-[#94A3B8]">{lead.email}</td>
                      <td className="px-4 py-2">
                        <span className="px-2 py-0.5 rounded text-xs bg-[#334155]">
                          {lead.status}
                        </span>
                      </td>
                      <td className="px-4 py-2">{lead.score}</td>
                      <td className="px-4 py-2 text-[#64748B]">
                        {lead.created_at
                          ? new Date(lead.created_at).toLocaleDateString()
                          : "-"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
