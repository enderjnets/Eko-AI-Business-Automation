"use client";

export default function ComingSoon() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-eko-graphite text-white px-6">
      <div className="max-w-xl text-center space-y-6">
        <div className="text-5xl">⚡️</div>
        <h1 className="text-4xl md:text-5xl font-bold">Eko AI</h1>
        <p className="text-lg text-gray-300">
          Business Automation con IA — sitio oficial próximamente.
        </p>
        <p className="text-sm text-gray-400">
          ¿Querés ver una demo en vivo del producto?{" "}
          <a
            className="text-eko-blue underline hover:text-blue-400"
            href="https://landing.ekoaiautomation.com/"
          >
            Mirá la landing page activa
          </a>
        </p>
        <p className="text-xs text-gray-500 pt-12">
          Eko AI Business Automation — Denver, CO
        </p>
      </div>
    </div>
  );
}
