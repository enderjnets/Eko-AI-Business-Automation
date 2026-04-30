import { Suspense } from "react";
import { Loader2 } from "lucide-react";
import BookDemoForm from "./BookDemoForm";

export default function BookDemoPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-eko-graphite flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-eko-blue" />
      </div>
    }>
      <BookDemoForm />
    </Suspense>
  );
}

// Server Component that wraps the client form
