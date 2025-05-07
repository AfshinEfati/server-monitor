<template>
    <div class="p-6">
      <div class="flex justify-between items-center mb-4">
        <h1 class="text-2xl font-bold">مدیریت سرورها</h1>
        <button @click="openCreateModal" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          ➕ افزودن سرور
        </button>
      </div>
  
      <!-- Search -->
      <input
        v-model="search"
        placeholder="جستجو بر اساس نام یا IP..."
        class="mb-4 w-full p-2 border border-gray-300 rounded"
      />
  
      <!-- DataTable -->
      <EasyDataTable
        :headers="headers"
        :items="filteredServers"
        :rows-per-page="10"
        @click-row="goToServerStats"
        table-class-name="custom-table"
      >
        <template #item-actions="{ item }">
          <div class="flex gap-2">
            <button @click.stop="openEditModal(item)" class="text-blue-600 hover:underline">✏️</button>
            <button @click.stop="deleteServer(item.id)" class="text-red-600 hover:underline">🗑️</button>
          </div>
        </template>
      </EasyDataTable>
  
      <!-- Modal -->
      <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-40 flex justify-center items-center z-50">
        <div class="bg-white p-6 rounded w-full max-w-md shadow-lg">
          <h2 class="text-xl font-bold mb-4">{{ editingServer ? 'ویرایش سرور' : 'افزودن سرور' }}</h2>
  
          <input v-model="form.name" placeholder="نام سرور" class="input mb-3" />
          <input v-model="form.ip" placeholder="IP" class="input mb-3" />
          <input v-model="form.ssh_user" placeholder="کاربر SSH" class="input mb-3" />
          <input v-model="form.ssh_password" placeholder="رمز SSH" type="password" class="input mb-3" />
  
          <div class="flex justify-end gap-2">
            <button @click="showModal = false" class="bg-gray-300 text-black px-4 py-2 rounded hover:bg-gray-400">
              بستن
            </button>
            <button @click="submitForm" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
              {{ editingServer ? 'ذخیره' : 'ایجاد' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  definePageMeta({
  layout: 'admin'
})
  import EasyDataTable from 'vue3-easy-data-table'
  const { token } = useAuth()
  const servers = ref([])
  const showModal = ref(false)
  const editingServer = ref(null)
  const form = reactive({ name: '', ip: '', ssh_user: '', ssh_password: '' })
  const search = ref('')
  
  const headers = [
    { text: 'ID', value: 'id' },
    { text: 'نام', value: 'name' },
    { text: 'IP', value: 'ip' },
    { text: 'کاربر SSH', value: 'ssh_user' },
    { text: 'عملیات', value: 'actions' }
  ]
  
  const fetchServers = async () => {
    servers.value = await $fetch('http://79.127.70.82:8042/servers', {
      headers: { Authorization: `Bearer ${token.value}` }
    })
  }
  
  const filteredServers = computed(() => {
    return servers.value.filter((s) =>
      s.name.toLowerCase().includes(search.value.toLowerCase()) ||
      s.ip.toLowerCase().includes(search.value.toLowerCase())
    )
  })
  
  const openCreateModal = () => {
    editingServer.value = null
    Object.assign(form, { name: '', ip: '', ssh_user: '', ssh_password: '' })
    showModal.value = true
  }
  
  const openEditModal = (server) => {
    editingServer.value = server
    Object.assign(form, { ...server })
    showModal.value = true
  }
  
  const submitForm = async () => {
    const url = editingServer.value
      ? `http://79.127.70.82:8042/servers/${editingServer.value.id}`
      : 'http://79.127.70.82:8042/servers'
  
    const method = editingServer.value ? 'PUT' : 'POST'
  
    await $fetch(url, {
      method,
      headers: {
        Authorization: `Bearer ${token.value}`,
        'Content-Type': 'application/json'
      },
      body: { ...form }
    })
  
    showModal.value = false
    await fetchServers()
  }
  
  const deleteServer = async (id) => {
    if (!confirm('حذف شود؟')) return
  
    await $fetch(`http://79.127.70.82:8042/servers/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token.value}` }
    })
  
    await fetchServers()
  }
  
  const router = useRouter()
  
  const goToServerStats = (server) => {
    router.push(`/servers/${server.id}/stats?name=${server.name}&ip=${server.ip}&ssh_user=${server.ssh_user}`)
  }
  
  onMounted(fetchServers)
  </script>
  
  <style scoped>
  .input {
    @apply w-full p-2 border border-gray-300 rounded outline-none focus:border-blue-500;
  }
  </style>
  