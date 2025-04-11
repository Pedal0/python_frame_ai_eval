/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/js/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6', // Blue-500
        secondary: '#10b981', // Emerald-500
        background: '#f3f4f6', // Gray-100
        surface: '#ffffff', // White
        textPrimary: '#1f2937', // Gray-800
        textSecondary: '#6b7280', // Gray-500
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out',
        'slide-in-bottom': 'slideInBottom 0.5s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideInBottom: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        }
      }
    },
  },
  plugins: [],
}