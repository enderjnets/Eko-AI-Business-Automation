"use client";

import Navbar from "@/components/Navbar";
import KanbanBoard from "@/components/KanbanBoard";

export default function PipelinePage() {
  return (
    <div className="min-h-screen bg-eko-graphite">
      <Navbar />
      <main className="pt-20 pb-12 px-4 sm:px-6 lg:px-8 max-w-[1600px] mx-auto">
        <div className="mb-6">
          <h1 className="text-2xl font-bold font-display">Sales Pipeline</h1>
          <p className="text-gray-400 text-sm mt-1">
            Drag leads through stages or use arrows to move them
          </p>
        </div>
        
        <KanbanBoard />
      </main>
    </div>
  );
}
