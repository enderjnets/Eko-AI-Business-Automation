"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import { X, Maximize, Minimize, AlertTriangle, Loader2, Play } from "lucide-react";

interface VideoModalProps {
  videoUrl: string;
  proxyUrl?: string;
  isOpen: boolean;
  onClose: () => void;
  title?: string;
}

// 1x1 transparent PNG as base64 fallback
const TRANSPARENT_PNG =
  "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==";

export default function VideoModal({ videoUrl, proxyUrl, isOpen, onClose, title }: VideoModalProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [useProxy, setUseProxy] = useState(false);

  const currentUrl = useProxy && proxyUrl ? proxyUrl : videoUrl;

  // Reset state when opening
  useEffect(() => {
    if (isOpen) {
      setIsLoading(true);
      setHasError(false);
      setUseProxy(false);
    }
  }, [isOpen]);

  // Close on Escape
  useEffect(() => {
    if (!isOpen) return;
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [isOpen, onClose]);

  // Track fullscreen changes
  useEffect(() => {
    const handler = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };
    document.addEventListener("fullscreenchange", handler);
    return () => document.removeEventListener("fullscreenchange", handler);
  }, []);

  const toggleFullscreen = useCallback(() => {
    const el = containerRef.current;
    if (!el) return;
    if (!document.fullscreenElement) {
      el.requestFullscreen().catch(() => {});
    } else {
      document.exitFullscreen().catch(() => {});
    }
  }, []);

  const handleVideoError = () => {
    if (!useProxy && proxyUrl) {
      setUseProxy(true);
      setIsLoading(true);
      setHasError(false);
    } else {
      setHasError(true);
      setIsLoading(false);
    }
  };

  const handleCanPlay = () => {
    setIsLoading(false);
    setHasError(false);
  };

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div
        ref={containerRef}
        className="relative w-full max-w-5xl mx-4 rounded-xl overflow-hidden bg-black border border-white/10 shadow-2xl"
        style={{ maxHeight: "85vh" }}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 bg-white/5 border-b border-white/5">
          <div className="flex items-center gap-2 min-w-0">
            {hasError ? (
              <AlertTriangle className="w-4 h-4 text-red-400 flex-shrink-0" />
            ) : (
              <Play className="w-4 h-4 text-pink-400 flex-shrink-0" />
            )}
            <span className="text-sm font-medium text-gray-200 truncate">
              {hasError ? "No se pudo cargar el video" : title || "Vista previa"}
            </span>
          </div>
          <div className="flex items-center gap-1 flex-shrink-0">
            <button
              onClick={toggleFullscreen}
              className="p-2 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
              title={isFullscreen ? "Salir de pantalla completa" : "Pantalla completa"}
            >
              {isFullscreen ? <Minimize className="w-4 h-4" /> : <Maximize className="w-4 h-4" />}
            </button>
            <button
              onClick={onClose}
              className="p-2 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
              title="Cerrar"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Video area */}
        <div className="relative flex items-center justify-center bg-black aspect-video">
          {isLoading && !hasError && (
            <div className="absolute inset-0 flex items-center justify-center z-10">
              <Loader2 className="w-8 h-8 animate-spin text-pink-400" />
            </div>
          )}

          {hasError ? (
            <div className="flex flex-col items-center justify-center gap-3 p-8 text-center">
              <AlertTriangle className="w-12 h-12 text-red-400/50" />
              <p className="text-sm text-gray-400 max-w-md">
                El video no está disponible. Probablemente el archivo expiró o fue eliminado del servidor.
              </p>
              {videoUrl && (
                <a
                  href={videoUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-pink-400 hover:text-pink-300 underline"
                >
                  Intentar abrir URL directa
                </a>
              )}
            </div>
          ) : (
            <video
              ref={videoRef}
              src={currentUrl}
              controls
              autoPlay
              className="w-full h-full max-h-[70vh] object-contain"
              onCanPlay={handleCanPlay}
              onError={handleVideoError}
              onLoadedData={handleCanPlay}
              poster={TRANSPARENT_PNG}
              playsInline
            />
          )}
        </div>
      </div>
    </div>
  );
}
