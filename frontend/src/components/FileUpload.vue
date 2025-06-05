<template>
  <div class="my-4">
    <input type="file" @change="onFileChange" class="mb-2" />
    <button @click="uploadFile" class="px-4 py-2 bg-blue-600 text-white rounded">업로드</button>
    <ProgressBar v-if="progress > 0" :value="progress" />
  </div>
</template>
<script setup>
import { ref } from 'vue'
import ProgressBar from './ProgressBar.vue'
import { useFileUpload } from '../composables/useFileUpload'

const { upload, progress } = useFileUpload()
const file = ref(null)
function onFileChange(e) { file.value = e.target.files[0] }
function uploadFile() { if (file.value) upload(file.value) }
</script>
