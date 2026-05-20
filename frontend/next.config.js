/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return {
      // beforeFiles: evaluated BEFORE Next.js checks filesystem pages.
      // Required for our host-based rewrite so `/` on landing.ekoaiautomation.com
      // doesn't get intercepted by the existing app/page.tsx (dashboard).
      beforeFiles: [
        {
          source: '/',
          has: [{ type: 'host', value: 'landing.ekoaiautomation.com' }],
          destination: '/landing',
        },
      ],
      // afterFiles: evaluated AFTER filesystem routing (default for normal rewrites).
      afterFiles: [
        {
          source: '/api/:path*',
          destination: 'http://eko-backend:8000/api/:path*',
        },
      ],
      fallback: [],
    };
  },
};

module.exports = nextConfig;
