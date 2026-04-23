/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        eko: {
          blue: '#0B4FD8',
          'blue-dark': '#0A3FB8',
          graphite: '#0F172A',
          green: '#10B981',
          white: '#F8FAFC',
        },
        gold: {
          DEFAULT: '#C9A84C',
          light: '#E8C97A',
          pale: '#F5E9C8',
        },
        rose: {
          DEFAULT: '#C47F8E',
          light: '#E8B4C0',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Plus Jakarta Sans', 'Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
