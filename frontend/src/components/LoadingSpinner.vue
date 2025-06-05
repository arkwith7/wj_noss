<template>
  <div
    v-if="loading"
    class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 flex items-center justify-center"
  >
    <div class="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-xl">
      <div class="flex flex-col items-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-lg font-medium text-gray-900 dark:text-white">{{ message }}</p>
        <p v-if="submessage" class="mt-2 text-sm text-gray-500 dark:text-gray-400">{{ submessage }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  loading: {
    type: Boolean,
    default: false
  },
  message: {
    type: String,
    default: 'Loading...'
  },
  submessage: {
    type: String,
    default: ''
  }
})
</script>
