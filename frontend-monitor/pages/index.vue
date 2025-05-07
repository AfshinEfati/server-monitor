<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        @submit.prevent="login"
        class="bg-white p-8 rounded shadow-md w-full max-w-md"
        autocomplete="off"
      >
        <h1 class="text-2xl font-bold mb-6 text-center">ورود به سیستم</h1>
  
        <label class="block mb-2 font-semibold">نام کاربری</label>
        <input
          v-model="username"
          type="text"
          placeholder="نام کاربری"
          class="input mb-4"
          autocomplete="new-username"
        />
  
        <label class="block mb-2 font-semibold">رمز عبور</label>
        <input
          v-model="password"
          type="password"
          placeholder="رمز عبور"
          class="input mb-4"
          autocomplete="new-password"
        />
  
        <button type="submit" class="btn mb-2">ورود</button>
  
        <p v-if="error" class="text-red-500 text-sm mt-2 text-center">{{ error }}</p>
      </form>
    </div>
  </template>
  
  <script setup>
  const username = ref('')
  const password = ref('')
  const error = ref('')
  const router = useRouter()
  const { setToken } = useAuth()
  
  const login = async () => {
    error.value = ''
  
    try {
      const res = await $fetch('http://79.127.70.82:8042/token', {
        method: 'POST',
        headers: {
         'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
          username: username.value,
          password: password.value
        })
      })
  
      setToken(res.access_token)
      router.push('/servers')
    } catch (err) {
      console.error('Login error:', err)
      error.value = 'ورود ناموفق بود. لطفاً اطلاعات را بررسی کنید.'
    }
  }
  </script>
  
  <style scoped>
  .input {
    @apply w-full p-2 border border-gray-300 rounded outline-none focus:border-blue-500;
  }
  .btn {
    @apply w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700;
  }
  </style>
  