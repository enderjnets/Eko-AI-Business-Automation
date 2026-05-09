/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        // Hardcoded to Docker internal network so server-side rewrites work inside the container.
        // Client-side fetch uses NEXT_PUBLIC_API_URL directly.
        destination: 'http://eko-backend:8000/api/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
