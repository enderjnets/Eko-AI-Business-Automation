"use client";

import { useState } from "react";
import { Zap, Loader2 } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";

export default function LoginPage() {
  const { login, devLogin } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);
    try {
      await login(email, password);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Login failed");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDevLogin = async () => {
    setError("");
    setIsLoading(true);
    try {
      await devLogin();
    } catch (err: any) {
      setError(err.response?.data?.detail || "Dev login failed");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-eko-graphite flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="flex items-center justify-center gap-3 mb-8">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-eko-blue to-eko-blue-dark flex items-center justify-center">
            <Zap className="w-6 h-6 text-white" />
          </div>
          <span className="font-display font-bold text-xl tracking-tight text-white">
            Eko <span className="text-eko-blue">AI</span>
          </span>
        </div>

        {/* Card */}
        <div className="rounded-2xl border border-white/10 bg-white/5 p-8 backdrop-blur-sm">
          <h1 className="text-xl font-bold text-white mb-2">Welcome back</h1>
          <p className="text-gray-400 text-sm mb-6">
            Sign in to your account to continue
          </p>

          {error && (
            <div className="mb-4 rounded-lg bg-red-500/10 border border-red-500/20 px-4 py-3 text-sm text-red-400">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 text-sm text-white placeholder-gray-500 focus:border-eko-blue focus:outline-none focus:ring-1 focus:ring-eko-blue"
                placeholder="you@company.com"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 text-sm text-white placeholder-gray-500 focus:border-eko-blue focus:outline-none focus:ring-1 focus:ring-eko-blue"
                placeholder="••••••••"
                required
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full rounded-lg bg-eko-blue px-4 py-2.5 text-sm font-semibold text-white hover:bg-eko-blue-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                "Sign In"
              )}
            </button>
          </form>

          <div className="mt-6">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-white/10" />
              </div>
              <div className="relative flex justify-center text-xs">
                <span className="bg-eko-graphite px-2 text-gray-500">or</span>
              </div>
            </div>

            <button
              onClick={handleDevLogin}
              disabled={isLoading}
              className="mt-4 w-full rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 text-sm font-medium text-gray-300 hover:bg-white/10 transition-colors disabled:opacity-50"
            >
              Dev Login (no credentials)
            </button>
          </div>
        </div>

        <p className="mt-6 text-center text-xs text-gray-500">
          Eko AI Business Automation — Denver, CO
        </p>
      </div>
    </div>
  );
}
