export default defineNuxtConfig({
    css: [
        '~/assets/css/tailwind.css',

    ],
    ssr: false,
    app: {
        baseURL: '/monitor/'
    },
    postcss: {
        plugins: {
            tailwindcss: {},
            autoprefixer: {},
            easydata: '~/plugins/vue3-easy-data-table.ts'
        },
    },
})