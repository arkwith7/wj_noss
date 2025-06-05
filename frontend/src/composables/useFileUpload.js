import { ref } from 'vue'
import { uploadFile } from '../services/uploadService'

export function useFileUpload() {
  const progress = ref(0)
  async function upload(file) {
    progress.value = 0
    await uploadFile(file)
    progress.value = 100
  }
  return { upload, progress }
}
