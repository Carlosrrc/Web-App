/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/**/*.css',
  ],
  theme: {
    extend: {
      colors: {
        // Custom colors for the dark theme if needed
      },
    },
  },
  darkMode: 'class', // Use 'class' for manual dark mode control
  plugins: [],
};
