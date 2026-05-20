"use client";

// www.ekoaiautomation.com + apex landing.
// The Next.js host-based rewrite in next.config.js sends / to /coming-soon
// when Host is www.* or apex. Render the full LandingPage marketing site
// (i18n + framer-motion) here.
import LandingPage from "@/components/LandingPage";

export default function Home() {
  return <LandingPage />;
}
