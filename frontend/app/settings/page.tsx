"use client";

import Navbar from "@/components/Navbar";
import { Settings, Shield, Bell, Key, Database } from "lucide-react";

export default function SettingsPage() {
  return (
    <div className="min-h-screen bg-eko-graphite">
      <Navbar />
      <main className="pt-20 pb-12 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-2xl font-bold font-display">Configuración</h1>
          <p className="text-gray-400 text-sm">Administra tu sistema de automatización</p>
        </div>

        <div className="space-y-6">
          {/* API Keys */}
          <div className="rounded-xl border border-white/5 bg-white/[0.02] p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 rounded-lg bg-eko-blue/10 text-eko-blue">
                <Key className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-medium">API Keys</h3>
                <p className="text-sm text-gray-500">Configura tus claves de servicios externos</p>
              </div>
            </div>
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-1">OpenAI API Key</label>
                <input
                  type="password"
                  placeholder="sk-..."
                  className="w-full rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 text-sm focus:border-eko-blue focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Resend API Key</label>
                <input
                  type="password"
                  placeholder="re_..."
                  className="w-full rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 text-sm focus:border-eko-blue focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Outscraper API Key</label>
                <input
                  type="password"
                  placeholder="..."
                  className="w-full rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 text-sm focus:border-eko-blue focus:outline-none"
                />
              </div>
            </div>
          </div>

          {/* Compliance */}
          <div className="rounded-xl border border-white/5 bg-white/[0.02] p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 rounded-lg bg-eko-green/10 text-eko-green">
                <Shield className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-medium">Cumplimiento</h3>
                <p className="text-sm text-gray-500">Configuraciones de TCPA, CAN-SPAM, CPA</p>
              </div>
            </div>
            <div className="space-y-3">
              <label className="flex items-center gap-3">
                <input type="checkbox" className="rounded border-white/20 bg-white/5" defaultChecked />
                <span className="text-sm">Validar DNC antes de cada contacto</span>
              </label>
              <label className="flex items-center gap-3">
                <input type="checkbox" className="rounded border-white/20 bg-white/5" defaultChecked />
                <span className="text-sm">Incluir divulgación de IA en emails</span>
              </label>
              <label className="flex items-center gap-3">
                <input type="checkbox" className="rounded border-white/20 bg-white/5" defaultChecked />
                <span className="text-sm">Footer unsubscribe obligatorio</span>
              </label>
            </div>
          </div>

          {/* Notifications */}
          <div className="rounded-xl border border-white/5 bg-white/[0.02] p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 rounded-lg bg-gold/10 text-gold">
                <Bell className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-medium">Notificaciones</h3>
                <p className="text-sm text-gray-500">Alertas y reportes automáticos</p>
              </div>
            </div>
            <div className="space-y-3">
              <label className="flex items-center gap-3">
                <input type="checkbox" className="rounded border-white/20 bg-white/5" defaultChecked />
                <span className="text-sm">Alerta cuando un lead responde</span>
              </label>
              <label className="flex items-center gap-3">
                <input type="checkbox" className="rounded border-white/20 bg-white/5" defaultChecked />
                <span className="text-sm">Reporte diario de rendimiento</span>
              </label>
              <label className="flex items-center gap-3">
                <input type="checkbox" className="rounded border-white/20 bg-white/5" />
                <span className="text-sm">Alerta de leads en riesgo de churn</span>
              </label>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
