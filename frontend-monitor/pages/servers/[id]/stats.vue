<template>
  <div class="p-6 space-y-6">
    <h1 class="text-2xl font-bold">📊 مانیتورینگ سرور: {{ server.name }}</h1>

    <!-- کارت‌های خلاصه -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <Card title="🖥️ CPU">{{ stats.cpu.usage_percent }}%</Card>
      <Card title="🧠 RAM">{{ stats.memory.usage_percent }}%</Card>
      <Card title="📶 Ping">{{ stats.ping }} ms</Card>
      <Card title="⏱️ Uptime">{{ stats.uptime }}</Card>
    </div>

    <!-- چارت‌ها -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- CPU چارت -->
      <div class="bg-white p-4 rounded shadow">
        <h2 class="font-semibold mb-2">CPU Usage (Live)</h2>
        <v-chart :option="cpuChart" class="h-64" />
      </div>

      <!-- RAM Pie -->
      <div class="bg-white p-4 rounded shadow">
        <h2 class="font-semibold mb-2">Memory Usage</h2>
        <v-chart class="h-64" :option="ramChart" autoresize />
      </div>

      <!-- Network chart -->
      <div class="bg-white p-4 rounded shadow col-span-1 md:col-span-2">
        <h2 class="font-semibold mb-2">Network RX / TX (MB)</h2>
        <v-chart class="h-64" :option="networkChart" autoresize />
      </div>
    </div>

    <!-- Disk list -->
    <div class="bg-white p-4 rounded shadow">
      <h2 class="font-semibold mb-2">Disk Usage</h2>
      <div v-for="disk in stats.disk" :key="disk.device" class="mb-4">
        <p class="text-sm font-medium">{{ disk.device }} - {{ disk.mountpoint }}</p>
        <div class="w-full bg-gray-200 h-4 rounded">
          <div
            class="bg-blue-500 h-4 rounded"
            :style="{ width: disk.usage_percent + '%' }"
          ></div>
        </div>
        <p class="text-xs text-gray-500 mt-1">
          {{ disk.used_gb }} / {{ disk.total_gb }} GB ({{ disk.usage_percent }}%)
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useIntervalFn } from '@vueuse/core'
import { ref, reactive, computed } from 'vue'
import VChart from 'vue-echarts'
import { useAuth } from '~/composables/useAuth'

definePageMeta({ layout: 'admin' })

const route = useRoute()
const id = route.params.id
const { token } = useAuth()

const server = reactive({
  name: route.query.name,
  ip: route.query.ip,
  ssh_user: route.query.ssh_user
})

const stats = ref({
  cpu: { usage_percent: 0 },
  memory: { usage_percent: 0, used_mb: 0, total_mb: 0 },
  network: { total_rx_mb: 0, total_tx_mb: 0 },
  disk: [],
  uptime: '',
  ping: 0
})

const cpuHistory = ref([])
const networkHistory = ref([])

const fetchStats = async () => {
  const res = await $fetch(`http://79.127.70.82:8042/servers/${id}/stats`, {
    headers: { Authorization: `Bearer ${token.value}` }
  })

  stats.value = res

  const now = new Date().toLocaleTimeString()

  cpuHistory.value.push({ name: now, value: res.cpu.usage_percent })
  networkHistory.value.push({
    time: now,
    rx: res.network.total_rx_mb,
    tx: res.network.total_tx_mb
  })

  if (cpuHistory.value.length > 20) cpuHistory.value.shift()
  if (networkHistory.value.length > 20) networkHistory.value.shift()
}

useIntervalFn(fetchStats, 3000, { immediate: true })

const cpuChart = computed(() => ({
  xAxis: {
    type: 'category',
    data: cpuHistory.value.map(p => p.name)
  },
  yAxis: { type: 'value', max: 100 },
  series: [
    {
      data: cpuHistory.value.map(p => p.value),
      type: 'line',
      smooth: true,
      areaStyle: {}
    }
  ],
  tooltip: { trigger: 'axis' }
}))

const ramChart = computed(() => ({
  tooltip: { formatter: '{b}: {d}%' },
  series: [
    {
      type: 'pie',
      radius: '70%',
      data: [
        { value: stats.value.memory.used_mb, name: 'Used' },
        {
          value:
            stats.value.memory.total_mb - stats.value.memory.used_mb,
          name: 'Free'
        }
      ]
    }
  ]
}))

const networkChart = computed(() => ({
  tooltip: { trigger: 'axis' },
  legend: { data: ['RX', 'TX'] },
  xAxis: {
    type: 'category',
    data: networkHistory.value.map(p => p.time)
  },
  yAxis: { type: 'value' },
  series: [
    {
      name: 'RX',
      type: 'line',
      data: networkHistory.value.map(p => p.rx),
      smooth: true
    },
    {
      name: 'TX',
      type: 'line',
      data: networkHistory.value.map(p => p.tx),
      smooth: true
    }
  ]
}))
</script>
