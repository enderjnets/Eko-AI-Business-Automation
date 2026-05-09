/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Removed API rewrites — frontend calls the backend directly via NEXT_PUBLIC_API_URL
};

module.exports = nextConfig;
