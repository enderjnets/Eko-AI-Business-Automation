export const CURRENT_VERSION = "0.1.0";

export interface VersionEntry {
  version: string;
  date: string;
  title: string;
  changes: string[];
}

export const CHANGELOG: VersionEntry[] = [
  {
    version: "0.1.0",
    date: "2026-05-05",
    title: "Inbox, DNS y Voice Agent",
    changes: [
      "Inbox agrupado por lead con conteo de mensajes",
      "Webhook de correos entrantes con auto-respuesta IA",
      "Formateo de correos: texto plano a HTML con párrafos y saltos de línea",
      "Pixel de tracking para apertura de correos",
      "Configuración DNS completa: SPF + DKIM + DMARC",
      "Soporte para Google Meet en reservas de demo",
      "Manejo de zona horaria en links de calendario (America/Denver)",
      "Conversaciones con threading vía in_reply_to",
      "Fix de RLS/workspace: migración de interacciones legacy",
      "Agente de voz VAPI con herramienta book_demo",
    ],
  },
];
