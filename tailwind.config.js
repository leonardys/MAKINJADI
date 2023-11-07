/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/templates/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [require("@tailwindcss/typography"), require("@tailwindcss/forms"), require("daisyui")],
  daisyui: {
    themes: ["light", "dark", "bumblebee"],
  },
}