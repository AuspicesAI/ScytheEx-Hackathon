/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        navy: "#0e2954",
        orange: "#f86302",
        purple: "#EF476F",
        grey: "#171717",
        offwhite: "#d9d9d9",
      },
    },
  },
  plugins: [],
};
