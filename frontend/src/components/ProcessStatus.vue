<template>
  <div class="my-4">
    <div v-if="status">처리 상태: {{ status }}</div>
    <ProgressBar v-if="progress > 0" :value="progress" />
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import ProgressBar from './ProgressBar.vue'
import { useProcessing } from '../composables/useProcessing'

const { status, progress, connectWebSocket } = useProcessing()
onMounted(connectWebSocket)
</script>
