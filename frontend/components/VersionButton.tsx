"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { GitCommit, X, History } from "lucide-react";
import { CURRENT_VERSION, CHANGELOG } from "@/lib/version";

export default function VersionButton() {
  const [open, setOpen] = useState(false);
  const overlayRef = useRef<HTMLDivElement>(null);
  const panelRef = useRef<HTMLDivElement>(null);

  const handleClose = useCallback(() => setOpen(false), []);

  // Close on ESC
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") handleClose();
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [open, handleClose]);

  // Close on click outside
  useEffect(() => {
    if (!open) return;
    const onClick = (e: MouseEvent) => {
      if (
        overlayRef.current &&
        panelRef.current &&
        !panelRef.current.contains(e.target as Node)
      ) {
        handleClose();
      }
    };
    // use timeout to avoid immediate close on the same click that opened
    const id = setTimeout(() => {
      document.addEventListener("mousedown", onClick);
    }, 0);
    return () => {
      clearTimeout(id);
      document.removeEventListener("mousedown", onClick);
    };
  }, [open, handleClose]);

  // Prevent body scroll when open
  useEffect(() => {
    if (open) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [open]);

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className="flex items-center gap-1.5 px-2 py-1 rounded-md text-xs font-medium bg-eko-blue/15 text-eko-blue hover:bg-eko-blue/25 transition-colors border border-eko-blue/20"
        title="Historial de versiones"
      >
        <GitCommit className="w-3 h-3" />
        <span>v{CURRENT_VERSION}</span>
      </button>

      {open && (
        <div
          ref={overlayRef}
          className="fixed inset-0 z-[60] flex items-center justify-center bg-black/60 backdrop-blur-sm animate-in fade-in duration-200"
        >
          <div
            ref={panelRef}
            className="relative w-full max-w-lg mx-auto max-h-[80vh] flex flex-col rounded-2xl border border-white/10 bg-eko-graphite shadow-2xl animate-in zoom-in-95 duration-200"
            role="dialog"
            aria-modal="true"
            aria-labelledby="version-modal-title"
          >
            {/* Header */}
            <div className="flex items-center justify-between px-5 py-4 border-b border-white/10">
              <div className="flex items-center gap-2">
                <History className="w-4 h-4 text-eko-blue" />
                <h2
                  id="version-modal-title"
                  className="text-base font-semibold text-white"
                >
                  Historial de versiones
                </h2>
              </div>
              <button
                onClick={handleClose}
                className="p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
                aria-label="Cerrar"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Body */}
            <div className="overflow-y-auto px-5 py-4 space-y-5">
              {CHANGELOG.map((entry) => (
                <div key={entry.version} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-bold bg-eko-blue/20 text-eko-blue border border-eko-blue/20">
                      v{entry.version}
                    </span>
                    <span className="text-xs text-gray-500">{entry.date}</span>
                  </div>
                  <h3 className="text-sm font-semibold text-gray-200">
                    {entry.title}
                  </h3>
                  <ul className="space-y-1.5">
                    {entry.changes.map((change, idx) => (
                      <li
                        key={idx}
                        className="flex items-start gap-2 text-sm text-gray-400"
                      >
                        <span className="mt-1.5 w-1 h-1 rounded-full bg-eko-blue shrink-0" />
                        <span>{change}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>

            {/* Footer */}
            <div className="px-5 py-3 border-t border-white/10 flex justify-end">
              <button
                onClick={handleClose}
                className="px-3 py-1.5 rounded-lg text-sm font-medium bg-white/10 text-white hover:bg-white/20 transition-colors"
              >
                Cerrar
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
