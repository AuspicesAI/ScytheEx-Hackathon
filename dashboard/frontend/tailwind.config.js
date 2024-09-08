/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          pink: "#EF476F",
          "brown-900": "#4b3f2d",
          "red-600": "#c53030",
          "orange-500": "#ed8936",
          "yellow-400": "#f6e05e",
        },
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
