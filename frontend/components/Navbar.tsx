"use client";

import { Zap, BarChart3, Users, Mail, Settings } from "lucide-react";
import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="glass fixed top-0 left-0 right-0 z-50 border-b border-white/5">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-eko-blue to-eko-blue-dark flex items-center justify-center">
              <Zap className="w-5 h-5 text-white" />
            </div>
            <span className="font-display font-bold text-lg tracking-tight">
              Eko <span className="text-eko-blue">AI</span>
            </span>
          </div>
          
          <div className="hidden md:flex items-center gap-1">
            <NavLink href="/" icon={<BarChart3 className="w-4 h-4" />} label="Dashboard" />
            <NavLink href="/leads" icon={<Users className="w-4 h-4" />} label="Leads" />
            <NavLink href="/campaigns" icon={<Mail className="w-4 h-4" />} label="Campañas" />
            <NavLink href="/settings" icon={<Settings className="w-4 h-4" />} label="Config" />
          </div>
          
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-eko-green animate-pulse" />
            <span className="text-xs text-gray-400">System Online</span>
          </div>
        </div>
      </div>
    </nav>
  );
}

function NavLink({ href, icon, label }: { href: string; icon: React.ReactNode; label: string }) {
  return (
    <Link
      href={href}
      className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-gray-400 hover:text-white hover:bg-white/5 transition-colors"
    >
      {icon}
      <span>{label}</span>
    </Link>
  );
}
