
export default defineNuxtConfig({
  css: [
    '~/assets/css/tailwind.css',
    
  ],
  
    postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
      easydata:'~/plugins/vue3-easy-data-table.ts'
    },
  },
})