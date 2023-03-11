/** @type {import('tailwindcss').Config} */

// const colors = require("tailwindcss/colors")

module.exports = {
  content: [
    "./templates/*.html",
    "./templates/**/*.html",
    "./templates/**/**/*.html",
    "./static/js/*.js",
    "./accounts/forms.py",
    "./plans/forms.py",
    "./profiles/forms.py",
    "./tex/forms.py",
  ],
  theme: {
    // colors: {
    //   primary: {"50":"#faf5ff","100":"#f3e8ff","200":"#e9d5ff","300":"#d8b4fe","400":"#c084fc","500":"#a855f7","600":"#9333ea","700":"#7e22ce","800":"#6b21a8","900":"#581c87"}
    // },
    extend: {},
  },
  plugins: [],
}
