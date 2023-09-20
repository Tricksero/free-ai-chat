/** @type {import('tailwindcss').Config} */

module.exports = {
  //purge: [
  //// Paths to your templates
  //"**/templates/**/*.html",
  //],
  content: ["**/templates/**/*.html", "!**/venv/**", "!**/node_modules/**"],
  theme: {
    extend: {
      colors: {
        "hhu-blue": "#006ab3",
        "hhu-blue-light": "#007bce",
        "hhu-blue-dark": "#01538a",
      },
    },
  },
  plugins: [],
};
