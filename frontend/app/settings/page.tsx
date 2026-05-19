"use client";

import { useState, useEffect, useCallback } from "react";
import Navbar from "@/components/Navbar";
import { useT } from "@/contexts/I18nProvider";
import {
  Settings,
  Shield,
  Bell,
  Key,
  UserCircle,
  Loader2,
  Save,
  CheckCircle,
  AlertCircle,
} from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { authApi, settingsApi } from "@/lib/api";

interface SettingItem {
  key: string;
  value: string;
  category: string;
  description?: string;
}

export default function SettingsPage() {
  const { user } = useAuth();
  const [currentPassword, setCurrentPassword] = useState("");
  const { t } = useT();
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [changing, setChanging] = useState(false);
  const [passwordMsg, setPasswordMsg] = useState("");

  const [settings, setSettings] = useState<Record<string, string>>({});
  const [loadingSettings, setLoadingSettings] = useState(true);
  const [savingKeys, setSavingKeys] = useState<Record<string, boolean>>({});
  const [saveMsgs, setSaveMsgs] = useState<Record<string, string>>({});

  const API_KEY_FIELDS = [
    { key: "OPENAI_API_KEY", label: "OpenAI API Key", placeholder: "sk-..." },
    { key: "RESEND_API_KEY", label: "Resend API Key", placeholder: "re_..." },
    { key: "OUTSCRAPER_API_KEY", label: "Outscraper API Key", placeholder: "..." },
    { key: "APIFY_API_KEY", label: "Apify API Key", placeholder: "..." },
    { key: "MINIMAX_API_KEY", label: "MiniMax API Key", placeholder: "..." },
    { key: "KIMI_API_KEY", label: "Kimi API Key", placeholder: "..." },
    { key: "RETELL_API_KEY", label: "Retell API Key", placeholder: "..." },
    { key: "VAPI_API_KEY", label: "Vapi API Key", placeholder: "..." },
    { key: "CAL_COM_API_KEY", label: "Cal.com API Key", placeholder: "..." },
  ];

  const COMPLIANCE_FIELDS = [
    { key: "DNC_VALIDATE_BEFORE_CONTACT", label: t("settings.compliance.dnc") },
    { key: "AI_DISCLOSURE_IN_EMAILS", label: t("settings.compliance.ai_disclosure") },
    { key: "UNSUBSCRIBE_FOOTER_REQUIRED", label: t("settings.compliance.unsubscribe_footer") },
  ];

  const NOTIFICATION_FIELDS = [
    { key: "ALERT_ON_LEAD_REPLY", label: t("settings.notif.lead_reply") },
    { key: "DAILY_PERFORMANCE_REPORT", label: t("settings.notif.daily_report") },
    { key: "ALERT_CHURN_RISK", label: t("settings.notif.churn_risk") },
  ];

  const loadSettings = useCallback(async () => {
    try {
      const res = await settingsApi.list();
      const map: Record<string, string> = {};
      (res.data as SettingItem[]).forEach((s) => {
        map[s.key] = s.value;
      });
      setSettings(map);
    } catch (err) {
      console.error("Failed to load settings:", err);
    } finally {
      setLoadingSettings(false);
    }
  }, []);

  useEffect(() => {
    loadSettings();
  }, [loadSettings]);

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setPasswordMsg("");
    if (newPassword !== confirmPassword) {
      setPasswordMsg(t("settings.password.mismatch"));
      return;
    }
    if (newPassword.length < 6) {
      setPasswordMsg(t("settings.password.too_short"));
      return;
    }
    setChanging(true);
    try {
      await authApi.updateMe({ password: newPassword });
      setPasswordMsg(t("settings.password.updated"));
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch (err: any) {
      setPasswordMsg(err.response?.data?.detail || t("settings.password.error"));
    } finally {
      setChanging(false);
    }
  };

  const updateSetting = async (key: string, value: string, category: string) => {
    setSavingKeys((prev) => ({ ...prev, [key]: true }));
    setSaveMsgs((prev) => ({ ...prev, [key]: "" }));
    try {
      await settingsApi.update(key, { value, category });
      setSettings((prev) => ({ ...prev, [key]: value }));
      setSaveMsgs((prev) => ({ ...prev, [key]: t("settings.saved") }));
      setTimeout(() => setSaveMsgs((prev) => ({ ...prev, [key]: "" })), 2000);
    } catch (err: any) {
      if (err.response?.status === 404) {
        // Create if not exists
        try {
          await settingsApi.create({ key, value, category });
          setSettings((prev) => ({ ...prev, [key]: value }));
          setSaveMsgs((prev) => ({ ...prev, [key]: t("settings.saved") }));
          setTimeout(() => setSaveMsgs((prev) => ({ ...prev, [key]: "" })), 2000);
        } catch (createErr: any) {
          setSaveMsgs((prev) => ({ ...prev, [key]: createErr.response?.data?.detail || t("settings.error") }));
        }
      } else {
        setSaveMsgs((prev) => ({ ...prev, [key]: err.response?.data?.detail || t("settings.error") }));
      }
    } finally {
      setSavingKeys((prev) => ({ ...prev, [key]: false }));
    }
  };

  const handleApiKeyChange = (key: string, value: string) => {
    setSettings((prev) => ({ ...prev, [key]: value }));
  };

  const handleApiKeyBlur = (key: string) => {
    updateSetting(key, settings[key] || "", "api_keys");
  };

  const toggleCheckbox = (key: string, category: string) => {
    const newValue = settings[key] === "true" ? "false" : "true";
    updateSetting(key, newValue, category);
  };

  const savedLabel = t("settings.saved");

  return (
    <div className="min-h-screen bg-eko-graphite">
      <Navbar />
      <main className="pt-20 pb-12 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-2xl font-bold font-display">{t("settings.title")}</h1>
          <p className="text-gray-400 text-sm">{t("settings.subtitle")}</p>
        </div>

        <div className="space-y-6">
          {/* Profile */}
          <div className="rounded-xl border border-white/5 bg-white/[0.02] p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 rounded-lg bg-eko-green/10 text-eko-green">
                <UserCircle className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-medium">{t("settings.profile.title")}</h3>
                <p className="text-sm text-gray-500">{user?.email} — {user?.role}</p>
              </div>
            </div>
            <form onSubmit={handleChangePassword} className="space-y-3">
              <div>
                <label className="block text-sm text-gray-400 mb-1">{t("settings.profile.new_password")}</label>
                <input
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  className="w-full rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 text-sm focus:border-eko-blue focus:outline-none"
                  placeholder="••••••••"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">{t("settings.profile.confirm_password")}</label>
                <input
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 text-sm focus:border-eko-blue focus:outline-none"
                  placeholder="••••••••"
                />
              </div>
              {passwordMsg && (
                <p className={`text-xs ${passwordMsg === t("settings.password.updated") ? "text-eko-green" : "text-red-400"}`}>
                  {passwordMsg}
                </p>
              )}
              <button
                type="submit"
                disabled={changing}
                className="rounded-lg bg-eko-blue px-4 py-2 text-sm font-medium hover:bg-eko-blue-dark disabled:opacity-50 transition-colors"
              >
                {changing ? <Loader2 className="w-4 h-4 animate-spin" /> : t("settings.profile.change_password")}
              </button>
            </form>
          </div>

          {/* API Keys */}
          <div className="rounded-xl border border-white/5 bg-white/[0.02] p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 rounded-lg bg-eko-blue/10 text-eko-blue">
                <Key className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-medium">{t("settings.api_keys.title")}</h3>
                <p className="text-sm text-gray-500">{t("settings.api_keys.subtitle")}</p>
              </div>
            </div>
            {loadingSettings ? (
              <div className="flex items-center justify-center py-8">
                <Loader2 className="w-6 h-6 animate-spin text-eko-blue" />
              </div>
            ) : (
              <div className="space-y-4">
                {API_KEY_FIELDS.map((field) => (
                  <div key={field.key}>
                    <div className="flex items-center justify-between mb-1">
                      <label className="block text-sm text-gray-400">{field.label}</label>
                      {saveMsgs[field.key] && (
                        <span className={`text-xs flex items-center gap-1 ${saveMsgs[field.key] === savedLabel ? "text-eko-green" : "text-red-400"}`}>
                          {saveMsgs[field.key] === savedLabel ? <CheckCircle className="w-3 h-3" /> : <AlertCircle className="w-3 h-3" />}
                          {saveMsgs[field.key]}
                        </span>
                      )}
                    </div>
                    <div className="relative">
                      <input
                        type="password"
                        value={settings[field.key] || ""}
                        onChange={(e) => handleApiKeyChange(field.key, e.target.value)}
                        onBlur={() => handleApiKeyBlur(field.key)}
                        placeholder={field.placeholder}
                        className="w-full rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 text-sm focus:border-eko-blue focus:outline-none pr-10"
                      />
                      {savingKeys[field.key] && (
                        <Loader2 className="absolute right-3 top-2.5 w-4 h-4 animate-spin text-gray-500" />
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Compliance */}
          <div className="rounded-xl border border-white/5 bg-white/[0.02] p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 rounded-lg bg-eko-green/10 text-eko-green">
                <Shield className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-medium">{t("settings.compliance.title")}</h3>
                <p className="text-sm text-gray-500">{t("settings.compliance.subtitle")}</p>
              </div>
            </div>
            <div className="space-y-3">
              {COMPLIANCE_FIELDS.map((field) => (
                <label key={field.key} className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    className="rounded border-white/20 bg-white/5 w-4 h-4"
                    checked={settings[field.key] === "true"}
                    onChange={() => toggleCheckbox(field.key, "compliance")}
                  />
                  <span className="text-sm">{field.label}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Notifications */}
          <div className="rounded-xl border border-white/5 bg-white/[0.02] p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 rounded-lg bg-gold/10 text-gold">
                <Bell className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-medium">{t("settings.notifications.title")}</h3>
                <p className="text-sm text-gray-500">{t("settings.notifications.subtitle")}</p>
              </div>
            </div>
            <div className="space-y-3">
              {NOTIFICATION_FIELDS.map((field) => (
                <label key={field.key} className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    className="rounded border-white/20 bg-white/5 w-4 h-4"
                    checked={settings[field.key] === "true"}
                    onChange={() => toggleCheckbox(field.key, "notifications")}
                  />
                  <span className="text-sm">{field.label}</span>
                </label>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
