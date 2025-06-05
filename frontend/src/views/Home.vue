<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">NOSS 교육과정 자동 생성 시스템</h1>
    <FileUpload />
    <ProcessStatus />
    <FileList />
  </div>
</template>
<script setup>
import FileUpload from '../components/FileUpload.vue'
import ProcessStatus from '../components/ProcessStatus.vue'
import FileList from '../components/FileList.vue'
</script>
