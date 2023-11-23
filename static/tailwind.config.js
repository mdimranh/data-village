/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../templates/**/*.html',
    './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {
      dropShadow: {
        'sm': '0 0 0.1rem rgba(0, 0, 0, 0.06)',
        'md': '0 0 0.2rem rgba(0, 0, 0, 0.12)',
        'lg': '0 0 0.3rem rgba(0, 0, 0, 0.18)',
        'xl': '0 0 0.4rem rgba(0, 0, 0, 0.24)',
        '2xl': '0 0 0.5rem rgba(0, 0, 0, 0.3)',
        '3xl': '0 0 0.6rem rgba(0, 0, 0, 0.36)',
        '4xl': '0 0 0.7rem rgba(0, 0, 0, 0.4)',
      }
    },
  },
  plugins: [
    require('flowbite/plugin')({
      charts: true,
    })
  ],
}

