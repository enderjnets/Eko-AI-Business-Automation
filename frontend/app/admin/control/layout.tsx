"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { Loader2 } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";

export default function ControlPlaneLayout({ children }: { children: React.ReactNode }) {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !user?.is_superuser) {
      router.replace("/");
    }
  }, [user, isLoading, router]);

  if (isLoading || !user?.is_superuser) {
    return (
      <div className="min-h-screen bg-eko-graphite flex items-center justify-center">
        <Loader2 className="w-6 h-6 animate-spin text-gray-500" />
      </div>
    );
  }

  return <>{children}</>;
}
