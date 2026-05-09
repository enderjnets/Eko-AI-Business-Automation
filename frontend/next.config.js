/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    // Proxy API calls to the backend container within the Docker network.
    // When accessed via nginx, nginx handles /api/* before it reaches Next.js.
    // When accessed directly (e.g. by IP), Next.js proxies to the backend.
    return [
      {
        source: '/api/:path*',
        destination: 'http://eko-backend:8000/api/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
