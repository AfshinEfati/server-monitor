<template>
    <div class="flex h-screen bg-gray-100">
      <!-- Sidebar -->
      <aside class="w-64 bg-white shadow-md flex flex-col">
        <div class="p-4 text-2xl font-bold border-b">🔧 Server Panel</div>
        <nav class="flex-1 p-4 space-y-2">
          <NuxtLink to="/dashboard" class="nav-link" active-class="bg-blue-100 text-blue-700">
            🏠 داشبورد
          </NuxtLink>
          <NuxtLink to="/servers" class="nav-link" active-class="bg-blue-100 text-blue-700">
            🖥️ سرورها
          </NuxtLink>
        </nav>
      </aside>
  
      <!-- Main Content -->
      <div class="flex-1 flex flex-col">
        <header class="bg-white shadow p-4 flex justify-between items-center">
          <div class="font-semibold text-lg">پنل مدیریت</div>
          <div>
            <button @click="logout" class="text-red-600 hover:underline">خروج</button>
          </div>
        </header>
        <main class="flex-1 overflow-y-auto p-6 bg-gray-50">
          <slot />
        </main>
      </div>
    </div>
  </template>
  
  <script setup>
  const router = useRouter()
  const { clearToken } = useAuth()
  
  const logout = () => {
    clearToken()
    router.push('/login')
  }
  </script>
  
  <style scoped>
  .nav-link {
    @apply block px-4 py-2 rounded hover:bg-gray-100 text-gray-700;
  }
  </style>
  