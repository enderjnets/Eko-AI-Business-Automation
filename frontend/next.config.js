/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return {
      // beforeFiles: evaluated BEFORE filesystem routes. Required so
      // host-based rewrites win over app/page.tsx and other concrete files.
      beforeFiles: [
        // landing.ekoaiautomation.com/ → renders the active LP component
        {
          source: '/',
          has: [{ type: 'host', value: 'landing.ekoaiautomation.com' }],
          destination: '/landing',
        },
        // www.ekoaiautomation.com/ + apex → placeholder "Coming Soon"
        {
          source: '/',
          has: [{ type: 'host', value: 'www.ekoaiautomation.com' }],
          destination: '/coming-soon',
        },
        {
          source: '/',
          has: [{ type: 'host', value: 'ekoaiautomation.com' }],
          destination: '/coming-soon',
        },
        // app.ekoaiautomation.com → no rewrite. / serves app/page.tsx
        // (Dashboard if auth, otherwise AuthContext redirects to /login).
      ],
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
