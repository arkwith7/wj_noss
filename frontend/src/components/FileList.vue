<template>
  <div class="my-4">
    <h2 class="font-semibold mb-2">생성된 파일 목록</h2>
    <ul>
      <li v-for="file in files" :key="file.name">
        <a :href="file.url" target="_blank" class="text-blue-600 underline">{{ file.name }}</a>
      </li>
    </ul>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useFileList } from '../composables/useFileList'

const { files, fetchFiles } = useFileList()
onMounted(fetchFiles)
</script>
