<template>
  <div class="w-full bg-gray-200 rounded h-4">
    <div class="bg-blue-500 h-4 rounded" :style="{ width: value + '%' }"></div>
  </div>
</template>
<script setup>
defineProps({ value: Number })
</script>
