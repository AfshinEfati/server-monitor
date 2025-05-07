<template>
  <div class="bg-white shadow rounded p-4">
    <h3 class="font-semibold mb-1 text-sm text-gray-500">{{ title }}</h3>
    <div class="text-xl font-bold text-gray-800"><slot /></div>
  </div>
</template>

<script setup>
defineProps({ title: String })
</script>
