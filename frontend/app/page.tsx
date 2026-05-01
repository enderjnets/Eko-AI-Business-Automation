"use client";

import { useState, useEffect } from "react";
import LandingPage from "@/components/LandingPage";
import Dashboard from "@/components/Dashboard";

export default function HomePage() {
  const [hasAuth, setHasAuth] = useState<boolean | null>(null);

  useEffect(() => {
    const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
    setHasAuth(!!token);
  }, []);

  if (hasAuth === null) {
    return (
      <div className="min-h-screen bg-eko-graphite flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-eko-blue border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return hasAuth ? <Dashboard /> : <LandingPage />;
}
