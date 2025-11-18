/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          start: '#667eea',
          end: '#764ba2',
        },
        card: {
          bg: 'rgba(42, 42, 42, 0.6)',
          header: 'rgba(51, 51, 51, 0.4)',
          content: 'rgba(30, 30, 30, 0.3)',
        },
      },
      backdropBlur: {
        20: '20px',
      },
    },
  },
  plugins: [],
}
