"use client";

import { LucideIcon } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  trend?: "up" | "down" | "neutral";
  color?: "blue" | "green" | "gold" | "rose";
}

export default function StatCard({ title, value, subtitle, icon: Icon, color = "blue" }: StatCardProps) {
  const colorClasses = {
    blue: "from-eko-blue/20 to-eko-blue/5 border-eko-blue/20",
    green: "from-eko-green/20 to-eko-green/5 border-eko-green/20",
    gold: "from-gold/20 to-gold/5 border-gold/20",
    rose: "from-rose/20 to-rose/5 border-rose/20",
  };

  const iconColors = {
    blue: "text-eko-blue",
    green: "text-eko-green",
    gold: "text-gold",
    rose: "text-rose",
  };

  return (
    <div className={`relative overflow-hidden rounded-xl border bg-gradient-to-br ${colorClasses[color]} p-6`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-gray-400">{title}</p>
          <p className="mt-2 text-3xl font-bold font-display">{value}</p>
          {subtitle && <p className="mt-1 text-xs text-gray-500">{subtitle}</p>}
        </div>
        <div className={`p-2 rounded-lg bg-white/5 ${iconColors[color]}`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>
    </div>
  );
}
