// /** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        'pythonYellow': '#ffde57',
        'pythonBlue': '#4584b6',
        'discordPurple': '#5865F2',
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
