"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { useRouter, usePathname } from "next/navigation";
import { authApi } from "@/lib/api";

interface User {
  id: number;
  email: string;
  full_name: string | null;
  role: string;
  is_active: boolean;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  devLogin: () => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const PUBLIC_PATHS = ["/login", "/book-demo", "/pricing", "/landing"];

// Hosts that run the SaaS dashboard. The auto-redirect to /login when
// unauthenticated only fires on these hosts. landing.* and www.* / apex are
// fully public — they serve dynamic LP / marketing and must not push to login.
const DASHBOARD_HOSTS = new Set<string>([
  "app.ekoaiautomation.com",
  // Dev / legacy direct hosts (preserve current behavior during migration)
  "localhost:3000",
  "localhost:3001",
  "100.88.47.99:3001",
]);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    const init = async () => {
      const token = localStorage.getItem("access_token");
      if (token) {
        try {
          const res = await authApi.me();
          setUser(res.data);
        } catch {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
        }
      }
      setIsLoading(false);
    };
    init();
  }, []);

  useEffect(() => {
    if (isLoading) return;
    const host = typeof window !== "undefined" ? window.location.host : "";
    const isDashboardHost = DASHBOARD_HOSTS.has(host);
    if (isDashboardHost && !user && !PUBLIC_PATHS.includes(pathname)) {
      router.push("/login");
    }
  }, [user, isLoading, pathname, router]);

  const login = async (email: string, password: string) => {
    const res = await authApi.login(email, password);
    const { access_token, refresh_token } = res.data;
    localStorage.setItem("access_token", access_token);
    localStorage.setItem("refresh_token", refresh_token);

    const meRes = await authApi.me();
    setUser(meRes.data);
    router.push("/");
  };

  const devLogin = async () => {
    const res = await authApi.devLogin();
    const { access_token, refresh_token } = res.data;
    localStorage.setItem("access_token", access_token);
    localStorage.setItem("refresh_token", refresh_token);

    const meRes = await authApi.me();
    setUser(meRes.data);
    router.push("/");
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUser(null);
    router.push("/login");
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, devLogin, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
