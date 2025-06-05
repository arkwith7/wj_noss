import { ref } from 'vue'
import { getFileList } from '../services/fileService'

export function useFileList() {
  const files = ref([])
  async function fetchFiles() {
    const res = await getFileList()
    files.value = res.data.files || []
  }
  return { files, fetchFiles }
}
